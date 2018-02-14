import uuid
import pkg_resources

import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


# Constants

BW_NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
TITAN_NAMD2 = 'namd2'

_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(eq0=100, eq1=5000, eq2=10, sim1=5000)
_full_steps = dict(eq0=1000, eq1=30000, eq2=800000, sim1=2000000)


class Esmacs(object):
    def __init__(self, number_of_replicas, systems, workflow=None, cores=16, full=False, cutoff=12.0):

        self.number_of_replicas = number_of_replicas
        self.systems = systems
        self.cores = cores
        self.step_count = _full_steps if full else _reduced_steps
        self.cutoff = cutoff
        self.id = uuid.uuid1()  # generate id

        self.workflow = workflow or ['eq0', 'eq1', 'eq2', 'sim1']
        
        # Profiler for ESMACS PoE

        self._uid = ru.generate_id('radical.htbac.esmacs')
        self._logger = ru.get_logger('radical.htbac.esmacs')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create esmacs instance', uid=self._uid)

    # Generate a new pipeline
    def generate_pipeline(self):

        pipeline = Pipeline()

        # Simulation stages
        # =================
        for step in self.workflow:
            stage = Stage()
            stage.name = step

            for system in self.systems:
                box = pmd.amber.AmberAsciiRestart('systems/esmacs/{s}/build/{s}-complex.crd'.format(s=system)).box

                for replica in range(self.number_of_replicas):

                    task = Task()
                    task.name = 'system_{}_replica_{}'.format(system, replica)

                    # Load namd module and set some environment variables.
                    task.pre_exec = ['module load namd/2.12',
                                     'export MPICH_PTL_SEND_CREDITS=-1',
                                     'export MPICH_MAX_SHORT_MSG_SIZE=8000',
                                     'export MPICH_PTL_UNEX_EVENTS=80000',
                                     'export MPICH_UNEX_BUFFER_SIZE=100M']

                    task.executable = [TITAN_NAMD2]
                    task.arguments += ['+ppn', str(self.cores-1),
                                       '+pemap', '1-{}'.format(self.cores-1),
                                       '+commap', '0',
                                       'esmacs-{}.conf'.format(step)]

                    task.copy_input_data = ['$SHARED/esmacs-{}.conf'.format(step)]

                    task.mpi = False
                    task.cores = self.cores

                    links = ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-cons.pdb'.format(system)]

                    if self.workflow.index(step):
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid,
                                                                       previous_task.uid)
                        links += [path + previous_stage.name + suffix for suffix in _simulation_file_suffixes]
                    else:
                        links += ['$SHARED/{}-complex.pdb'.format(system)]

                    task.link_input_data = links

                    settings = dict(BOX_X=box[0], BOX_Y=box[1], BOX_Z=box[2], SYSTEM=system, STEP=self.step_count[step],
                                    CUTOFF=self.cutoff, SWITCHING=self.cutoff-2.0, PAIRLISTDIST=self.cutoff+1.5)

                    task.pre_exec += ["sed -i 's/{}/{}/g' *.conf".format(k, w) for k, w in settings.items()]

                    stage.add_tasks(task)

            pipeline.add_stages(stage)

        print 'HTBAC: ESM pipeline has', len(pipeline.stages), 'stages.'
        print 'HTBAC: Tasks per stage:', [len(s.tasks) for s in pipeline.stages]
        print 'HTBAC: {} system(s), {} replica(s).'.format(len(self.systems), self.number_of_replicas)
        print 'HTBAC: Total cores required: {}, i.e. {} nodes.'.format(self.total_cores, self.total_cores/16)

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = [pkg_resources.resource_filename(__name__, 'default-configs/esmacs-{}.conf'.format(step)) for step in self.workflow]
        for system in self.systems:
            files += ['default_configs/esmacs-{}.conf'.format(step) for step in self.workflow]
            files += ['systems/esmacs/{s}/build/{s}-complex.pdb'.format(s=system)]
            files += ['systems/esmacs/{s}/build/{s}-complex.top'.format(s=system)]
            files += ['systems/esmacs/{s}/constraint/{s}-cons.pdb'.format(s=system)]
        return files

    @property
    def total_cores(self):
        return self.cores * self.number_of_replicas * len(self.systems)
