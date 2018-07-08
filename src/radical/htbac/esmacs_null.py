import parmed as pmd
import uuid

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
# NAMD_MMPBSA_ANALYSIS = "WHERE IS IT?"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(eq0=1000, eq1=5000, eq2=5000, sim1=50000)
_full_steps = dict(eq0=1000, eq1=30000, eq2=970000, sim1=2000000)


class Esmacs_null(object):
    
    def __init__(self, number_of_replicas, systems = list(), cores = 32, workflow = None, full = False):

        self.number_of_replicas = number_of_replicas
        self.systems = systems
        self.cores = cores
        self.step_count = _reduced_steps
        self._id = uuid.uuid1()  # generate id
        self.workflow = workflow or ['eq0', 'eq1', 'eq2', 'sim1']
        
        # Profiler for ESMACS PoE

        self._uid = ru.generate_id('radical.htbac.esmacs')
        self._logger = ru.get_logger('radical.htbac.esmacs')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create esmacs instance', uid=self._uid)

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
            for system in self.systems: 
                # self.box = pmd.amber.AmberAsciiRestart('systems/esmacs/{s}/build/{s}-complex.crd'.format(s=system)).box
                for replica in range(self.number_of_replicas):
                
                    task = Task()
                    task.name = 'system_{}_replica_{}'.format(system, replica)

                    # task.pre_exec = ['module load namd/2.12',
                    #                  'export MPICH_PTL_SEND_CREDITS=-1',
                    #                  'export MPICH_MAX_SHORT_MSG_SIZE=8000',
                    #                  'export MPICH_PTL_UNEX_EVENTS=80000',
                    #                  'export MPICH_UNEX_BUFFER_SIZE=100M',
                    #                  'export OMP_NUM_THREADS=1']

                    # cpu_reqs are arguments for aprun                                 
                    # cpu_reps = {-n processing elements (PEs) defined as 'processes', 
                    #             process type (MPI) defines as 'process_type', 
                    #             -d (depth) specifies the number of threads i.e. the
                    #             number of processors per node for each PE defined as 'threads_per_process'}
                    # ** each application is given -n * -d cores      

                    #task.cpu_reqs = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 16, 'thread_type': None}
                    task.arguments = ['I am task']

                    task.executable = ['/bin/echo']
                    # task.copy_input_data = ['$SHARED/esmacs-{}.conf'.format(stage.name)]
                    
                    # aprun -n $NPROC -N 1 -d 8 namd2 +ppn 7 +setcpuaffinity \ 
                    # +pemap 0,2,4,6,8,10,12 +commap 14 +idlepoll +devices 0 \
                    # sim.conf > sim.log 2>&1

                    # task.cpu_reqs = {'processes': 1, 'process_type': None, 'threads_per_process': 1, 'thread_type': None} GPU stack only

                    task.mpi = True
                    task.cores = self.cores

                    links = []
                    links += ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-cons.pdb'.format(system)]

                    if self.workflow.index(step):
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid,
                                                                       previous_task.uid)
                        # links += [path + previous_stage.name + suffix for suffix in _simulation_file_suffixes]
                    else:
                        links += ['$SHARED/{}-complex.pdb'.format(system)]

                    task.link_input_data = links

                    # task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.box[0]),
                    #                   "sed -i 's/BOX_Y/{}/g' *.conf".format(self.box[1]),
                    #                   "sed -i 's/BOX_Z/{}/g' *.conf".format(self.box[2]),
                    #                   "sed -i 's/SYSTEM/{}/g' *.conf".format(system)]

                    # task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[step])]

                    stage.add_tasks(task)

            pipeline.add_stages(stage)

        print 'ESM pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = []
        files += ['default_configs/esmacs-{}.conf'.format(step) for step in self.workflow]
        for system in self.systems: 
            files += ['systems/esmacs/{s}/build/{s}-complex.pdb'.format(s=system)]
            files += ['systems/esmacs/{s}/build/{s}-complex.top'.format(s=system)]
            files += ['systems/esmacs/{s}/constraint/{s}-cons.pdb'.format(s=system)]
        return files

    @property
    def total_replicas(self):
        return self.number_of_replicas*len(self.systems)
    @property
    def total_cores(self):
        return self.number_of_replicas*self.cores*len(self.systems)

