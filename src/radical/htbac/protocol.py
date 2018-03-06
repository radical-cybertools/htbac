# Protocol class

import uuid
import pkg_resources

import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task

# constants
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(eq0=100, eq1=5000, eq2=10, sim1=5000)
_full_steps = dict(eq0=1000, eq1=30000, eq2=800000, sim1=2000000)


class Protocol(object):
    def __init__(self, 
            protocol = None, 
            replicas = 0, 
            systems = list(), 
            workflow = None, 
            cores=0,
            full = False, 
            lambdas = 1, 
            **kwargs):

    self.protocol = protocol
    self.replicas = replicas
    self.systems = systems
    self.cores = cores
    self.step_count = _full_steps if full else _reduced_steps
    self.workflow = workflow or ['eq0', 'eq1', 'eq2', 'sim1']
    self.cutoff = kwargs.get('cutoff', 12.0)
    self.water_model = kwargs.get('water_model', 'tip3')
    self.id = uuid.uuid1()  # generate id

        # Esmacs parameters
    # =================

    self.cutoff = kwargs.get('cutoff', 12.0)
    self.water_model = kwargs.get('water_model', 'tip3')


    # Input data
    # =================

    @property
    def input_data(self):
    files = [pkg_resources.resource_filename(__name__, 'default-configs/esmacs-{}.conf'.format(step)) for step in self.workflow]
    for system in self.systems:
        files += ['systems/{s}/build/{s}-complex.pdb'.format(s=system)]
        files += ['systems/{s}/build/{s}-complex.top'.format(s=system)]
        files += ['systems/{s}/constraint/{s}-cons.pdb'.format(s=system)]
    return files

    # Protocol
    # =================

    @property
    def total_cores(self):
    return self.cores * self.number_of_replicas * len(self.systems) * len(self.lambdas)

def Esmacs(self):

    ## To Do: create .json to obtain resource specific parameters
    # currently: supporting BW

    # constants

    NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'

    pipeline = Pipeline()

        # Simulation stages
        # =================

    for step in self.workflow:
        stage = Stage()
        stage.name = step

        for system in self.systems:
            box = pmd.amber.AmberAsciiRestart('systems/{s}/build/{s}-complex.inpcrd'.
                            format(s=system)).box

            for replica in range(self.number_of_replicas):

                task = Task()
                task.name = 'system_{}_replica_{}'.format(system, 
                                    replica)

                task.pre_exec += ["sed -i 's/{}/{}/g' *.conf".format(k, w) for k, w in settings.items()]
                task.executable = [NAMD2]
                task.arguments += ['esmacs-{}.conf'.format(step)]

                task.copy_input_data = ['$SHARED/esmacs-{}.conf'.format(step)]

                task.mpi = True
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

                    settings = dict(BOX_X=box[0], BOX_Y=box[1], BOX_Z=box[2], SYSTEM=system,
                                STEP=self.step_count[step], CUTOFF=self.cutoff, SWITCHING=self.cutoff-2.0,
                                PAIRLISTDIST=self.cutoff+1.5, WATERMODEL=self.water_model)


            stage.add_tasks(task)

        pipeline.add_stages(stage)

    return pipeline

    print 'HTBAC: ESM pipeline has', len(pipeline.stages), 'stages.'
    print 'HTBAC: Tasks per stage:', [len(s.tasks) for s in pipeline.stages]
    print 'HTBAC: {} system(s), {} replica(s).'.format(len(self.systems), self.number_of_replicas)
    print 'HTBAC: Total cores required: {}, i.e. {} nodes.'.format(self.total_cores, self.total_cores/16)

    

if self.protocol == 'esmacs':

    # self._uid = ru.generate_id('radical.htbac.protocol')
    # self._logger = ru.get_logger('radical.htbac.protocol')
    # self._prof = ru.Profiler(name=self._uid)
    # self._prof.prof('create protocol instance', uid=self._uid)
    
    Esmacs() 

# if self.protocol = 'ties':


#     # self._uid = ru.generate_id('radical.htbac.protocol')
#     # self._logger = ru.get_logger('radical.htbac.protocol')
#     # self._prof = ru.Profiler(name=self._uid)
#     # self._prof.prof('create protocol instance', uid=self._uid)

#     Ties()  




