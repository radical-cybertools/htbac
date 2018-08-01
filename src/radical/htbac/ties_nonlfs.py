import numpy as np
import parmed as pmd
import uuid

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(min=1000, eq1=5000, eq2=5000, prod=50000)
_full_steps = dict(min=1000, eq1=30000, eq2=970000, prod=2000000)


class Ties(object):

    def __init__(self, number_of_replicas, number_of_windows, systems = list(), 
        cores=32, workflow=None, ligand=False, full=False, additional=list()):

        self.number_of_replicas = number_of_replicas
        self.lambdas = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        self.lambdas = np.append(self.lambdas, additional or [0.05, 0.95])
        self.ligand = '-ligands' if ligand else ''
        self.step_count = _full_steps if full else _reduced_steps
        
        self.systems = systems
        # print "Lambda Windows: ", self.lambdas
        # print "step count: ", self.step_count 

        self.cores = cores
        self._id = uuid.uuid1()  # generate id

        self.workflow = workflow or ['min', 'eq1', 'eq2', 'prod']
        
        # Profiler for TIES PoE

        self._uid = ru.generate_id('radical.htbac.ties')
        self._logger = ru.get_logger('radical.htbac.ties')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create ties instance', uid=self._uid)

    def id(self):
        return self._id

    # Generate a new pipeline
    def generate_pipeline(self):

        pipeline = Pipeline()
        pipeline.name = 'p1'
        # Simulation stages
        # =================

        
        stage_0 = Stage()
        stage_0.name = self.workflow[0]
        print stage_0.name

           
        for system in self.systems:  
            box = pmd.amber.AmberAsciiRestart('systems/ties{lig}/{s}/build/{s}-complex.crd'.format(lig=self.ligand, s=system)).box
            for replica in range(self.number_of_replicas):
                for ld in self.lambdas:

                    task = Task()
                    task.name = 'system-{}-replica-{}-lambda-{}'.format(system, replica, ld)
                    task.arguments = ['+pemap', '0-31']
                    task.arguments += ['ties-{}.conf'.format(self.workflow[0])]
                    task.copy_input_data = ['$SHARED/ties-{}.conf'.format(self.workflow[0])]
                    task.executable = [NAMD2]
                    # task.lfs_per_process = self.number_of_replicas*len(self.lambdas)*len(self.systems)
                    task.cpu_reqs = { 
                            'processes': 32,
                            'process_type': 'MPI',
                            'threads_per_process': 1,
                            'thread_type': None
                        }

                    links = []
                    links += ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-tags.pdb'.format(system)]
                    if self.workflow.index(self.workflow[0]):
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.name, previous_stage.name, previous_task.name)
                        links += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
                    else:
                        links += ['$SHARED/{}-complex.pdb'.format(system)]

                    print "Linking files:", links
                    task.link_input_data = links

                    task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(box[0]),
                                      "sed -i 's/BOX_Y/{}/g' *.conf".format(box[1]),
                                      "sed -i 's/BOX_Z/{}/g' *.conf".format(box[2]),
                                      "sed -i 's/SYSTEM/{}/g' *.conf".format(system)]

                    task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[self.workflow[0]])]

                    task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

                    stage_0.add_tasks(task)

        pipeline.add_stages(stage_0)

        stage_1 = Stage()
        stage_1.name = self.workflow[1]
        print stage_1.name

           
        for system in self.systems:  
            box = pmd.amber.AmberAsciiRestart('systems/ties{lig}/{s}/build/{s}-complex.crd'.format(lig=self.ligand, s=system)).box
            for replica in range(self.number_of_replicas):
                for ld in self.lambdas:

                    task = Task()
                    task.name = 'system-{}-replica-{}-lambda-{}'.format(system, replica, ld)
                    task.arguments = ['+pemap', '0-31']
                    task.arguments += ['ties-{}.conf'.format(self.workflow[1])]
                    task.copy_input_data = ['$SHARED/ties-{}.conf'.format(self.workflow[1])]
                    task.executable = [NAMD2]
                    # task.tag = task.name
                    task.cpu_reqs = { 
                            'processes': 32,
                            'process_type': 'MPI',
                            'threads_per_process': 1,
                            'thread_type': None
                        }

                    links = []
                    links += ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-tags.pdb'.format(system)]
                    if self.workflow.index(self.workflow[1]):
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.name, previous_stage.name, previous_task.name)
                        links += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
                    else:
                        links += ['$SHARED/{}-complex.pdb'.format(system)]

                    print "Linking files:", links
                    task.link_input_data = links

                    task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(box[0]),
                                      "sed -i 's/BOX_Y/{}/g' *.conf".format(box[1]),
                                      "sed -i 's/BOX_Z/{}/g' *.conf".format(box[2]),
                                      "sed -i 's/SYSTEM/{}/g' *.conf".format(system)]

                    task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[self.workflow[1]])]

                    task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

                    stage_1.add_tasks(task)


        pipeline.add_stages(stage_1)
            
        # Analysis stage
        # ==============
        # analysis = Stage()
        # analysis.name = 'analysis'

        # for replica in range(self.number_of_replicas):
        #     analysis_task = Task()
        #     analysis_task.name = 'replica_{}'.format(replica)

        #     analysis_task.arguments += ['-d', '*ti.out', '>', 'dg_{}.out'.format(analysis_task.name)]
        #     analysis_task.executable = [NAMD_TI_ANALYSIS]

        #     analysis_task.mpi = False
        #     analysis_task.cores = 1

        #     for p in filter(None, [pipeline, previous_pipeline]):
        #         production_stage = next(stage for stage in p.stages if stage.name == 'prod')
        #         production_tasks = [t for t in production_stage.tasks if analysis_task.name in t.name]
        #         links = ['$Pipeline_{}_Stage_{}_Task_{}/alch_{}_ti.out'.format(p.uid, production_stage.uid, t.uid, t.name.split('_lambda_')[-1]) for t in production_tasks]
        #         analysis_task.link_input_data += links

        #     analysis.add_tasks(analysis_task)

        # pipeline.add_stages(analysis)

        # # Averaging stage
        # # ===============
        # average = Stage()
        # average.name = 'average'

        # average_task = Task()
        # average_task.name = 'average_dg'
        # average_task.arguments = ['-1 --quiet dg_* > dgs.out']  # .format(pipeline.uid)]
        # average_task.executable = ['head']

        # average_task.mpi = False
        # average_task.cores = 1

        # previous_stage = pipeline.stages[-1]
        # previous_tasks = previous_stage.tasks

        # links = ['$Pipeline_{}_Stage_{}_Task_{}/dg_{}.out'.format(pipeline.uid, previous_stage.uid, t.uid,
        #                                                           t.name) for t in previous_tasks]
        # average_task.link_input_data = links
        # #average_task.download_output_data = ['dgs.out']  # .format(pipeline.uid)]

        # average.add_tasks(average_task)
        # pipeline.add_stages(average)


        print 'TIES pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]
        return pipeline

    # Input data
    @property
    def input_data(self):
        files = ['default_configs/ties-{}.conf'.format(step) for step in self.workflow]
        for system in self.systems: 
            files += ['systems/ties{lig}/{s}/build/{s}-complex.pdb'.format(lig=self.ligand, s=system)]
            files += ['systems/ties{lig}/{s}/build/{s}-complex.top'.format(lig=self.ligand, s=system)]
            files += ['systems/ties{lig}/{s}/build/{s}-tags.pdb'.format(lig=self.ligand, s=system)]
        return files

    @property
    def total_replicas(self):
        return self.number_of_replicas*len(self.lambdas)*len(self.systems)
    @property
    def total_cores(self):
        return self.number_of_replicas*len(self.lambdas)*self.cores*len(self.systems)
