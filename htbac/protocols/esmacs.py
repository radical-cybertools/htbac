import os
import uuid
from pkg_resources import resource_filename

import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


# Constants
_reduced_steps = [100, 5000, 1000, 10, 5000]
_full_steps = [1000, 30000, 1000, 800000, 2000000]


class Esmacs(object):
    def __init__(self, number_of_replicas, systems, rootdir, cores, full, numsteps=5,  **kwargs):

        self.cores = cores
        self.id = uuid.uuid1()
        self.systems = systems
        self.numsteps = numsteps
        self.rootdir = os.path.abspath(rootdir)
        self.number_of_replicas = number_of_replicas
        self.step_count = _full_steps if full else _reduced_steps

        self.cutoff = kwargs.get('cutoff', 10.0)
        self.water_model = kwargs.get('water_model', 'tip4')

        self.engine = dict()
        
        # Profiler for ESMACS PoE

        self._uid = ru.generate_id('radical.htbac.esmacs')
        self._logger = ru.get_logger('radical.htbac.esmacs')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create esmacs instance', uid=self._uid)

    def set_engine_for_resource(self, resource):
        # This version of ESMACS uses NAMD to run the simulations.
        self.engine = resource['namd']

    def generate_task(self, system, replica, step, box, data):

        task = Task()
        task.name = self.get_task_name(system, replica)

        task.pre_exec = self.engine['pre_exec']
        task.executable = self.engine['executable']['openmp_cuda']
        task.arguments = self.engine['arguments']
        task.mpi = self.engine['uses_mpi']
        task.cores = self.engine['cores'] or self.cores

        task.arguments += ['esmacs-{}.conf'.format(step)]

        task.copy_input_data = ['$SHARED/esmacs-{}.conf'.format(step)]

        task.post_exec = ['echo stage:{}-{} > simulation.desc'.format(step, task.name)]

        task.link_input_data = ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-cons.pdb'.format(system)] + data[1]

        settings = dict(BOX_X=box[0], BOX_Y=box[1], BOX_Z=box[2], SYSTEM=system,
                        STEP=self.step_count[step], CUTOFF=self.cutoff, SWITCHING=self.cutoff-2.0,
                        PAIRLISTDIST=self.cutoff+1.5, WATERMODEL=self.water_model,
                        INPUT=data[0], OUTPUT=self.get_stage_name(step))

        task.pre_exec += ["sed -i 's/{}/{}/g' *.conf".format(k, w) for k, w in settings.items()]

        return task

    def generate_pipeline(self):

        pipeline = Pipeline()
        pipeline.name = 'esmacs'

        for step in range(self.numsteps):
            stage = Stage()
            stage.name = self.get_stage_name(step)

            for system in self.systems:
                comps = [self.rootdir] + system.split('-') + [system]
                base = os.path.join(*comps)
                box = pmd.amber.AmberAsciiRestart(base+'-complex.inpcrd').box

                for replica in range(self.number_of_replicas):

                    if step > 0:
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == self.get_task_name(system, replica))
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.name, previous_stage.name,
                                                                       previous_task.name)
                        data = (previous_stage.name, [path + previous_stage.name + suffix for suffix in ['.coor', '.xsc', '.vel']])
                    else:
                        data = ('', ['$SHARED/{}-complex.pdb'.format(system)])

                    task = self.generate_task(system, replica, step, box, data)
                    stage.add_tasks(task)

            pipeline.add_stages(stage)

        print 'HTBAC: ESM pipeline has', len(pipeline.stages), 'stages.'
        print 'HTBAC: Tasks per stage:', [len(s.tasks) for s in pipeline.stages]
        print 'HTBAC: {} system(s), {} replica(s).'.format(len(self.systems), self.number_of_replicas)
        print 'HTBAC: Total cores required: {}, i.e. {} nodes.'.format(self.total_cores, self.total_cores/16)

        return pipeline


from ..protocol import Protocol
from ..simulation import EnsembleSimulation


class Esmacs(Protocol):
    def __init__(self):
        super(Esmacs, self).__init__()

        s0 = EnsembleSimulation()
        s0.config = resource_filename(__name__, 'default-configs/esmacs-0.conf')
        s0.add_ensemble('replica', range(25))
        s0.engine = 'namd_openmp_cuda'

        s1 = EnsembleSimulation()
        s1.config = resource_filename(__name__, 'default-configs/esmacs-1.conf')

        self.add_simulation(s1)
