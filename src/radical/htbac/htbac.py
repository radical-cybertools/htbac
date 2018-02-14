import json
import pprint
import pkg_resources

import radical.utils as ru
from radical.entk import AppManager, ResourceManager

__copyright__ = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__ = "Jumana Dakka <jumanadakka@gmail.com>, Kristof Farkas-Pall <kristofarkas@gmail.com>"
__license__ = "MIT"


class Runner(object):
    def __init__(self, supercomputer='titan'):
        self.supercomputer = supercomputer
        self._protocols = list()
        self._hostname = None
        self._port = None
        self.ids = None
        self.app_manager = None

        # Profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create workflow_runner obj', uid=self._uid)
        self._root_directories = list()
        self.ids = dict()

    def add_protocol(self, protocol):
        self._protocols.append(protocol)

    def rabbitmq_config(self, hostname='localhost', port=5672):
        self._hostname = hostname
        self._port = port

    def run(self, strong_scaled=1, autoterminate=True, queue='batch', walltime=120, dry_run=False):
        pipelines = set()
        input_data = list()
        cores = 0

        for protocol in self._protocols:
            gen_pipeline = protocol.generate_pipeline()
            pipelines.add(gen_pipeline)
            input_data.extend(protocol.input_data)
            self.ids[protocol.id] = gen_pipeline
            # protocol.id is the uuid, gen_pipeline.uid is the pipeline

            cores += protocol.total_cores

        cores *= strong_scaled
        cores += 16  # Additional node for agent.

        res_dict = self.resource_dictionary(cores, queue, walltime)

        print 'HTBAC RUNNER: using a total of {} cores.'.format(cores)
        print 'HTBAC RUNNER: Resource dictionary:'
        pprint.pprint(res_dict)

        # Create Resource Manager object with the above resource description
        resource_manager = ResourceManager(res_dict)
        resource_manager.shared_data = input_data

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

    def resource_dictionary(self, cores, queue, walltime):
        resource = json.load(pkg_resources.resource_stream(__name__, 'resources.json'))[self.supercomputer]

        resource['cores'] = cores
        resource['queue'] = queue
        resource['walltime'] = walltime

        return resource
