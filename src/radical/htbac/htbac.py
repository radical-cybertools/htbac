__copyright__   = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__      = "Jumana Dakka <jumanadakka@gmail.com>, Kristof Farkas-Pall <kristofarkas@gmail.com>"
__license__     = "MIT"

import os

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
 

class Runner(object):
    def __init__(self):
        self._cores = 0
        self._protocols = list()
        self._hostname = None
        self._port = None
        self.ids = None
        self.app_manager = None
        self.total_replicas = 0
        self.instances = None

        # Profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create workflow_runner obj', uid=self._uid)
        self._root_directories = list()
        self.ids = dict()

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


    def PoE(self):

        pipelines = set()
        input_data = list()

        for protocol in self._protocols:

            gen_pipeline = protocol.generate_pipeline()
            self.ids[protocol.id()] = gen_pipeline
            self.replicas += protocol.replicas
            pipelines.add(gen_pipeline)
            input_data.extend(protocol.input_data)
            

        # Here we combine all pipelines into a single pipeline

        p = Pipeline() 
    
        for index,s in enumerate(pipelines[0].stages):
            stage = Stage()
            for pipeline in pipelines:
                stage.add_tasks(pipeline.stages[index].tasks)
            p.add_stages(stage)

        print 'Creating', len(p.stages.tasks), 'tasks.'
        print 'Creating', len(p.stages), 'stages.'
        print 'Creating', len(p), 'pipeline.'
        return p

    def run(self, strong_scaled=1):

        # Create Application Manager
        self.app_manager = AppManager(hostname=self._hostname, port=self._port)
        self.app_manager.assign_workflow(self.PoE())
        # Pilot size   
        self._cores = self._cores * self.replicas 
        
        print 'Running on', self._cores, 'cores.'

        res_dict = {'resource': 'ncsa.bw_aprun',
                    'walltime': 1440,
                    'cores': int(self._cores*strong_scaled),
                    'project': 'bamm',
                    'queue': 'high',
                    'access_schema': 'gsissh'}

        # Create Resource Manager object with the above resource description
        resource_manager = ResourceManager(res_dict)
        resource_manager.shared_data = input_data
        self.app_manager.resource_manager = resource_manager

        self._prof.prof('execution_run')
        print 'Running...'
        self.app_manager.run()    # this method is blocking until all pipelines show state = completed

    
