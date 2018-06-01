import sys
import yaml
import pprint
import logging
from pkg_resources import resource_stream

import radical.utils as ru
from radical.entk import AppManager, ResourceManager

from .simulation import Simulatable

__copyright__ = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__ = "Jumana Dakka <jumanadakka@gmail.com>, Kristof Farkas-Pall <kristofarkas@gmail.com>"
__license__ = "MIT"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Runner(object):
    def __init__(self, resource='local', comm_server=None):
        """The workhorse of high throughput binding affinity calculations.

        Manages arbitrary number of protocols on any resource (including supercomputers).

        Parameters
        ----------
        resource: str
            The name of the resource where the protocols will be run. This is usually then name of the supercomputer
            or 'local' if the job will be executed locally. (the default is to try to run locally).
        comm_server: tuple(str, int)
            The communication server used by the execution system. Specify a hostname and port number as a tuple. If
            None, then the dedicated server might be used from the resource description if present.
        """

        self.resource = yaml.load(resource_stream(__name__, 'resources.yaml'))[resource]

        if comm_server is None:
            comm_server = self.resource.get('dedicated_rabbitmq_server')

        self._protocols = list()
        self._app_manager = AppManager(*comm_server)

        # Profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create workflow_runner obj', uid=self._uid)
        self._root_directories = list()

    def add_protocol(self, protocol):
        """Add a new protocol to the list of protocols to be executed.

        Parameters
        ----------
        protocol: Simulatable
        """
        protocol.configure_engine_for_resource(self.resource)
        self._protocols.append(protocol)

    def run(self, resource=None, walltime=None, strong_scaled=1, queue=None, access_schema=None, dry_run=False):
        """Run protocols.

        Parameters
        ----------
        resource: str
            The specific resource and sub-resource you want to use.
        walltime: int
            Wall time in minutes.
        strong_scaled: float
            For testing strong scaling. Number of cores will be multiplied by this number before execution.
        queue: str
            Name of the queue. If there is a default for your resource that will be used.
        access_schema: str
            One of ssh, gsissh, local
        dry_run: bool
            Whether to execute the `.run` command or not.
        """

        pipelines = set()
        shared_data = set()
        cores = 0

        max_cu_count = self.resource.get('max_cu_count', 0)

        for protocol in self._protocols:
            gen_pipeline = protocol.generate_pipeline()

            cu_count = len(gen_pipeline.stages[0].tasks)
            if max_cu_count and cu_count > max_cu_count:
                raise ValueError('Resource allows up to {} concurrent CUs. You have {}.'.format(max_cu_count, cu_count))

            pipelines.add(gen_pipeline)
            shared_data.update(protocol.shared_data)
            cores += protocol.cores

        cores *= strong_scaled
        cores += self.resource.get('agent_cores', 0)

        self.resource['resource_dictionary']['cores'] = cores

        if resource:
            self.resource['resource_dictionary']['resource'] = resource
        if walltime:
            self.resource['resource_dictionary']['walltime'] = walltime
        if queue:
            self.resource['resource_dictionary']['queue'] = queue
        if access_schema:
            self.resource['resource_dictionary']['access_schema'] = access_schema

        logger.info('Using total number of cores: {}.'.format(cores))
        logger.info('Resource dictionary:\n{}'.format(pprint.pformat(self.resource['resource_dictionary'])))

        # Create Resource Manager object with the above resource description
        resource_manager = ResourceManager(self.resource['resource_dictionary'])
        resource_manager.shared_data = list(shared_data)

        # Create Application Manager
        self._app_manager.resource_manager = resource_manager
        self._app_manager.assign_workflow(pipelines)

        logger.info("\n".join("Stage {}: {}*{} cores.".
                              format(i, len(s.tasks), next(iter(s.tasks)).cores)
                              for i, s in enumerate(next(iter(pipelines)).stages)))

        self._prof.prof('execution_run')
        logger.info('Running workflow.')

        if not dry_run:
            self._app_manager.run()    # this method is blocking until all pipelines show state = completed

    def rerun(self, protocol=None, terminate=True, previous_pipeline=None):

        if self.ids.get(previous_pipeline.id(), None) is not None:

            pipelines = set()

            gen_pipeline = protocol.generate_pipeline(previous_pipeline=self.ids[previous_pipeline.id()])

            pipelines.add(gen_pipeline)

            self.ids[protocol.id] = gen_pipeline

            self.app_manager.assign_workflow(pipelines)

            self.app_manager.run()

            if terminate:
                self.app_manager.resource_terminate()

        else: 

            print "ERROR: previous protocol instance is not found"
