import numpy as np
import parmed as pmd
import uuid

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


# openMM = $PATH
# ANALYSIS_MBAR = $PATH
# _simulation_file_suffixes = ['.coor', '.xsc', '.vel'] # check if this will become pdb or stay as YAML
# _reduced_steps = dict(min=1000, eq1=5000, eq2=5000, prod=50000) 
# _full_steps = dict(min=1000, eq1=30000, eq2=970000, prod=2000000)

NULL = ['bin/sleep']

class Yank(object):

    def __init__(self, number_of_replicas,
                 systems=list(), 
                 workflow=None, 
                 cores=32, 
                 ligand=False, 
                 full=False,
                 gibbs_steps,
                 thermodynamic_states):

        self.number_of_replicas = number_of_replicas
        self.n_gibbs_steps =  gibbs_steps
        self.thermo_state = thermodynamic_states
        self.ligand = '-ligands' if ligand else ''
        self.step_count = _full_steps if full else _reduced_steps
        
        self.systems = systems
        
        self.cores = cores
        self._id = uuid.uuid1()  # generate id

        # self.workflow = workflow or ['gen_replicas', 'repex', 'rotation', 'translation', 'propagation']
        
        # null workflow
        self.workflow = workflow or list(range(0,5)) 


        # Profiler for TIES PoE

        self._uid = ru.generate_id('radical.yank.yank-repex')
        self._logger = ru.get_logger('radical.yank.yank-repex')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create yank-repex instance', uid=self._uid)

    def id(self):
        return self._id

    # Generate a new pipeline
    def generate_pipeline(self):

        pipeline = Pipeline()

        # generate replicas
        # create a wrapper task that assigns the values of replica_i and replica_j
        # =================

        stage_1 = Stage() 

        for _gibbs_step in range(self.n_gibbs_steps): 

            task = Task() # assign replica_i and replica_j
            task.name = assign_replica_numbers

            task.executable = [NULL]
            task.cores = self.cores
            task.arguments = ['I am task %s'%_gibbs_step]
            stage_1.add_tasks(task)


        pipeline.add_stages(stage_1)

        # replica exchange Metropolis criteria
        # invoke repex from RepEx 3.0 
        # =================

        stage_2 = Stage()

        for _gibbs_step in range(self.n_gibbs_steps): 
        
            task = Task()
            task.name = repex 

            task.executable = [NULL]
            task.cores = self.cores
            task.arguments = ['I am task %s'%_gibbs_step]
            stage_2.add_tasks(task)

        pipeline.add_stages(stage_2)

        # rotation (MC) 
        # =================

        stage_3 = Stage()

        for replica in range(self.number_of_replicas):

            task = Task()
            task.name = rotation  

            task.executable = [NULL]
            task.cores = self.cores
            task.arguments = ['I am task %s'%replica]
            stage_3.add_tasks(task)

        pipeline.add_stages(stage_3)

        # translation (MC)
        # =================

        stage_4 = Stage()

        
        for replica in range(self.number_of_replicas):

            task = Task()
            task.name = rotation  

            task.executable = [NULL]
            task.cores = self.cores
            task.arguments = ['I am task %s'%replica]
            stage_4.add_tasks(task)

        pipeline.add_stages(stage_4)

        # propagation (MC)
        # =================

        stage_5 = Stage()

        for replica in range(self.number_of_replicas):

            task = Task()
            task.name = rotation  

            task.executable = [NULL]
            task.cores = self.cores
            task.arguments = ['I am task %s'%replica]
            stage_5.add_tasks(task)

        pipeline.add_stages(stage_5)

        # energy matrix 
        # for every replica pull the sampler state
        # compute the energy matrix of each thermo state in thermo_matrix, given that replica's sampler state
        # =================

        stage_6 = Stage()

        for replica in range(self.number_of_replicas):

            for thermo_state in range(self.thermo_state)

                task = Task()
                task.name = rotation  

                task.executable = [NULL]
                task.cores = self.cores
                task.arguments = ['I am task %s'%replica]
                stage_6.add_tasks(task)

        pipeline.add_stages(stage_6)


        print 'TIES pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]
        return pipeline

    
    @property
    def replicas(self):
        return self.number_of_replicas