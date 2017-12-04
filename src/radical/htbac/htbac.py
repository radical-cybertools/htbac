__copyright__   = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__      = "Jumana Dakka <jumanadakka@gmail.com>"
__license__     = "MIT"

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os

class Runner(object):

    def __init__(self):

        self._cores = 0
        self._protocols = list()
        self._res_dict = None
        self._hostname = None
        self._port = None
        self.total_replicas = 0

        #profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name = self._uid) 
        self._prof.prof('create wkflw_runner obj', uid=self._uid)
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
            raise TypeError(expected_type=int, actual_type=type(val))


    @property
    def res_dict(self):

        return self._res_dict

    
    def rabbitmq_config(self, hostname = 'localhost', port = 5672):

        self._hostname = hostname
        self._port = port

    def run(self):

        pipelines = set()

        for p in self._protocols:
            pipelines.add(p.generate_pipeline())
            self._root_directories.append(p.input_data)
            self.total_replicas+=p.replicas
            


        self.input_tgzs = list()
        for directory in self._root_directories:
            self.input_tgzs.append(directory+ '.tgz')   #if .tgz is available it will use .tgz
            for subdir, dirs, files in os.walk(directory):
                for file in files:
                    print os.path.join(subdir, file)

        
        res_dict = {'resource': 'ncsa.bw_aprun',
                   'walltime': 1440,
                   'cpus': self._cores*self.total_replicas,
                   'project': 'bamm',
                   'queue': 'high',
                   'access_schema': 'gsissh'}




        # Create Resource Manager object with the above resource description
        rman = ResourceManager(res_dict)
        rman.shared_data = self.input_tgzs
        # Create Application Manager
        appman = AppManager(hostname = self._hostname, port = self._port)

        # Assign resource manager to the Application Manager
        appman.resource_manager = rman

        # Assign the workflow as a set of Pipelines to the Application Manager
        appman.assign_workflow(pipelines)

        # Run the Application Manager
        self._prof.prof('execution_run')
        appman.run()

'''
        res_dict = {'resource': 'local.localhost',
                   'walltime': 1440,
                   'cpus': self._cores,
                   'project': ''}

        res_dict = {'resource': 'ncsa.bw_aprun',
                   'walltime': 1440,
                   'cpus': self._cores*self.total_replicas,
                   'project': 'bamm',
                   'queue': 'high',
                   'access_schema': 'gsissh'}

        new function:

        self.input_root_directory = list()

        for directory in self._root_directories: 
            for subdir, dirs, files in os.walk(directory):
                for file in files:
                    self.input_root_directory.append(os.path.join(subdir, file))

        # don't forget to pass self.input_root_directory to shared_data


        
'''

