import numpy as np
import parmed as pmd
import uuid

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
TITAN_NAMD2 = 'namd2'
TITAN_ORTE_NAMD2 = '/lustre/atlas2/csc230/world-shared/openmpi/applications/namd/namd-openmp/CRAY-XE-gnu/namd2'

NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(min=1000, eq1=5000, eq2=5000, prod=50000)
_full_steps = dict(min=1000, eq1=30000, eq2=970000, prod=2000000)

class Ties(object):

    def __init__(self, number_of_replicas, number_of_windows=0, additional=list(),
                 systems=list(), workflow=None, cores=16, ligand=False, full=False):

        self.number_of_replicas = number_of_replicas
        self.lambdas = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        self.lambdas = np.append(self.lambdas, additional or [0.05, 0.95])
        self.ligand = '-ligands' if ligand else ''
        self.step_count = _full_steps if full else _reduced_steps
        
        self.systems = systems
        print "Lambda Windows: ", self.lambdas
        print "stage count: ", self.step_count

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

        # Simulation stages
        # =================

        for step in self.workflow:
            stage = Stage()
            stage.name = step
            print stage.name

            for system in self.systems:
                box = pmd.amber.AmberAsciiRestart('systems/ties{lig}/{s}/build/{s}-complex.crd'.format(lig=self.ligand, s=system)).box
                    
                for replica in range(self.number_of_replicas):
                    for ld in self.lambdas:
                    
                        task = Task()
                        task.name = 'system_{}_replica_{}_lambda_{}'.format(system, replica, ld)

                        task.copy_input_data = ['$SHARED/ties-{}.conf'.format(stage.name)]
                        # task.pre_exec = ['module load namd/2.12',
                        #          'export MPICH_PTL_SEND_CREDITS=-1',
                        #          'export MPICH_MAX_SHORT_MSG_SIZE=8000',
                        #          'export MPICH_PTL_UNEX_EVENTS=80000',
                        #          'export MPICH_UNEX_BUFFER_SIZE=100M',
                        #          'export OMP_NUM_THREADS=1']

                        task.pre_exec = ['export LD_PRELOAD=/lib64/librt.so.1',
                                        'module swap PrgEnv-pgi PrgEnv-gnu/5.2.82',
                                        'module load tcl_tk/8.5.8',
                                        'module unload cray-mpich',
                                        'module load cmake',
                                        'module load rca',
                                        'module load python/2.7.9',
                                        'module load python_pip/8.1.2',
                                        'module load python_virtualenv/12.0.7']

                        task.cpu_reqs = {'processes': 1, 'threads_per_process': 16}
                        # task.cpu_reqs = {'process_type': 'MPI'}

                        task.arguments += ['+ppn', '15', 'ties-{}.conf'.format(stage.name)]
                        # task.arguments += ['+ppn', '14', '+pemap', '0-13',
                        #                    '+commap', '14', 'ties-{}.conf'.format(stage.name)]

                        task.executable = [TITAN_ORTE_NAMD2]         
                        task.mpi = False
                        # task.cores = self.cores

                        links = []
                        links += ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-tags.pdb'.format(system)]
                        if self.workflow.index(step):
                            previous_stage = pipeline.stages[-1]
                            previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                            path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid, previous_task.uid)
                            links += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
                        else:
                            links += ['$SHARED/{}-complex.pdb'.format(system)]

                        # print "Linking files:", links
                        task.link_input_data = links

                        task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(box[0]),
                                          "sed -i 's/BOX_Y/{}/g' *.conf".format(box[1]),
                                          "sed -i 's/BOX_Z/{}/g' *.conf".format(box[2]),
                                          "sed -i 's/SYSTEM/{}/g' *.conf".format(system)]

                        task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[step])]

                        task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

                        stage.add_tasks(task)

            pipeline.add_stages(stage)
            
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
    def replicas(self):
        return self.number_of_replicas * len(self.lambdas) * len(self.systems)

    @property
    def total_cores(self):
        return self.cores * self.number_of_replicas * len(self.systems) * len(self.lambdas) 