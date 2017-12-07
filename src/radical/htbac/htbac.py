__copyright__   = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__      = "Jumana Dakka <jumanadakka@gmail.com>, Kristof Farkas-Pall <kristofarkas@gmail.com>"
__license__     = "MIT"

import radical.utils as ru
from radical.entk import AppManager, ResourceManager


class Runner(object):
    def __init__(self):
        self._cores = 0
        self._protocols = list()
        self._hostname = None
        self._port = None
        self.total_replicas = 0

        # Profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create workflow_runner obj', uid=self._uid)
        self._root_directories = list()

    def add_protocol(self, protocol):
        self._protocols.append(protocol)

    @property
    def cores(self):
        return self._cores

    @cores.setter
    def cores(self, val):
        if isinstance(val, int):
            self._cores = val
        else:
            raise TypeError()

    def rabbitmq_config(self, hostname='localhost', port=5672):
        self._hostname = hostname
        self._port = port

    def run(self, walltime=1440, strong_scaled=1):
        pipelines = set()
        input_data = list()

        for protocol in self._protocols:
            pipelines.add(protocol.generate_pipeline())
            input_data.extend(protocol.input_data)
            self.total_replicas += protocol.replicas

        self._cores = self._cores * self.total_replicas
        print 'Running on', self._cores, 'cores.'

        res_dict = {'resource': 'ncsa.bw_aprun',
                    'walltime': walltime,
                    'cores': int(self._cores*strong_scaled),
                    'project': 'bamm',
                    'queue': 'high',
                    'access_schema': 'gsissh'}

        # Create Resource Manager object with the above resource description
        resource_manager = ResourceManager(res_dict)
        resource_manager.shared_data = input_data

        # Create Application Manager
        app_manager = AppManager(hostname=self._hostname, port=self._port)
        app_manager.resource_manager = resource_manager
        app_manager.assign_workflow(pipelines)

        self._prof.prof('execution_run')
        print 'Running...'
        app_manager.run()



