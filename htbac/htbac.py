import yaml
import pprint
from pkg_resources import resource_stream

import radical.utils as ru
from radical.entk import AppManager, ResourceManager

__copyright__ = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__ = "Jumana Dakka <jumanadakka@gmail.com>, Kristof Farkas-Pall <kristofarkas@gmail.com>"
__license__ = "MIT"


class Runner(object):
    def __init__(self, resource):

        self.resource = yaml.load(resource_stream(__name__, 'resources.yaml'))[resource]

        self._protocols = list()
        self._hostname = None
        self._port = None
        self.app_manager = None

        # Profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create workflow_runner obj', uid=self._uid)
        self._root_directories = list()

    def add_protocol(self, protocol):
        protocol.set_engine_for_resource(self.resource)
        self._protocols.append(protocol)

    def rabbitmq_config(self, hostname='openshift-node1.ccs.ornl.gov', port=30673):
        self._hostname = hostname
        self._port = port

    def run(self, walltime=None, strong_scaled=1, queue=None, dry_run=False):

        pipelines = set()
        shared_data = set()
        cores = 0

        for protocol in self._protocols:
            gen_pipeline = protocol.generate_pipeline()
            pipelines.add(gen_pipeline)
            shared_data.update(protocol.shared_data)
            cores += protocol.cores

        cores *= strong_scaled
        cores += self.resource.get('agent_cores', 0)

        self.resource['resource_dictionary']['cores'] = cores
        self.resource['resource_dictionary']['walltime'] = walltime
        if queue:
            self.resource['resource_dictionary']['queue'] = queue

        print 'HTBAC RUNNER: using a total of {} cores.'.format(cores)
        print 'HTBAC RUNNER: Resource dictionary:'
        pprint.pprint(self.resource['resource_dictionary'])

        # Create Resource Manager object with the above resource description
        resource_manager = ResourceManager(self.resource['resource_dictionary'])
        resource_manager.shared_data = list(shared_data)

        # Create Application Manager
        self.app_manager = AppManager(hostname=self._hostname, port=self._port)
        self.app_manager.resource_manager = resource_manager
        self.app_manager.assign_workflow(pipelines)

        self._prof.prof('execution_run')
        print 'Running...'

        if not dry_run:
            self.app_manager.run()    # this method is blocking until all pipelines show state = completed

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
