__copyright__   = "Copyright 2017-2018, http://radical.rutgers.edu"
__author__      = "Jumana Dakka <jumanadakka@gmail.com>, Kristof Farkas-Pall <kristofarkas@gmail.com>"
__license__     = "MIT"

import os

import radical.utils as ru
from radical.entk import AppManager

class Runner(object):
    def __init__(self):
        self._cores = 0
        self._protocols = list()
        self._hostname = None
        self._port = None
        self.ids = None
        self.app_manager = None
        self.total_replicas = 0
        self._cores = 0

        # Profiler for Runner
        self._uid = ru.generate_id('radical.htbac.workflow_runner')
        self._logger = ru.get_logger('radical.htbac.workflow_runner')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create workflow_runner obj', uid=self._uid)
        self._root_directories = list()
        self.ids = dict()

    def add_protocol(self, protocol):
        self._protocols.append(protocol)

    # @property
    # def cores(self):
    #     return self._cores

    # @cores.setter
    # def cores(self, val):
    #     if isinstance(val, int):
    #         self._cores = val
    #     else:
    #         raise TypeError()

    def rabbitmq_config(self, hostname='localhost', port=5672):
        self._hostname = hostname
        self._port = port


    def run(self, strong_scaled = 1, autoterminate = True, queue = 'compute',
            walltime = 60):
        pipelines = set()
        input_data = list()

        for protocol in self._protocols:
            gen_pipeline = protocol.generate_pipeline()
            pipelines.add(gen_pipeline)
            input_data.extend(protocol.input_data)
            self.ids[protocol.id()] = gen_pipeline
            # protocol.id is the uuid, gen_pipeline.uid is the pipeline

            # self.total_replicas += protocol.replicas
            self._cores += protocol.total_cores
            self.total_replicas += protocol.total_replicas
        #self._cores = self._cores * self.total_replicas
        print 'Running on', self._cores, 'cores with', self.total_replicas, 'replicas'

        res_dict = {'resource': 'xsede.comet',
                    'walltime': walltime,
                    'cpus': int(self._cores*strong_scaled),
                    'project': 'unc100',
                    'queue': queue,
                    'access_schema': 'gsissh'}

        # res_dict = {'resource': 'ncsa.bw_aprun',
        #             'walltime': walltime,
        #             'cpus': int(self._cores*strong_scaled),
        #             'project': 'bamm',
        #             'queue': queue,
        #             'access_schema': 'gsissh'}

        # res_dict = {'resource': 'ornl.titan_aprun',
        #             'walltime': walltime,
        #             'cpus': int(self._cores*strong_scaled),
        #             'project': 'CHM126',
        #             'queue': queue,
        #             'access_schema': 'local'}

        # Create Application Manager
        self.app_manager = AppManager(hostname=self._hostname, port=self._port)
        self.app_manager.resource_desc = res_dict
        self.app_manager.workflow = pipelines
        self.app_manager.shared_data = input_data

        self._prof.prof('execution_run')
        print 'Running...'
        self.app_manager.run()    # this method is blocking until all pipelines show state = completed


    def rerun(self, protocol=None, terminate=True, previous_pipeline=None):

        if self.ids.get(previous_pipeline.id(), None) is not None:
            pipelines = set()
            gen_pipeline = protocol.generate_pipeline(previous_pipeline=self.ids[previous_pipeline.id()])
            pipelines.add(gen_pipeline)
            self.ids[protocol.id()] = gen_pipeline
            self.app_manager.assign_workflow(pipelines)
            self.app_manager.run()
            if terminate:
                self.app_manager.resource_terminate()

        else: 

            print "ERROR: previous protocol instance is not found"

