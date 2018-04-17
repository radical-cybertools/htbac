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

        self.number_of_replicas = number_of_replicas
        self.systems = systems
        self.rootdir = os.path.abspath(rootdir)
        self.cores = cores
        self.numsteps = numsteps
        self.step_count = _full_steps if full else _reduced_steps
        self.id = uuid.uuid1()  # generate id

        self.cutoff = kwargs.get('cutoff', 10.0)
        self.water_model = kwargs.get('water_model', 'tip4')

        self.engine = dict()
        
        # Profiler for ESMACS PoE

        self._uid = ru.generate_id('radical.htbac.esmacs')
        self._logger = ru.get_logger('radical.htbac.esmacs')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create esmacs instance', uid=self._uid)

    def set_engine_for_resource(self, resource):
        self.engine = resource['namd']

    # Generate a new pipeline
    def generate_pipeline(self):

        pipeline = Pipeline()
        pipeline.name = 'esmacs'

        # Simulation stages
        # =================
        for step in range(self.numsteps):
            stage = Stage()
            stage.name = 'stage-{}'.format(step)

            for system in self.systems:
                comps = [self.rootdir] + system.split('-') + [system]
                base = os.path.join(*comps)
                box = pmd.amber.AmberAsciiRestart(base+'-complex.inpcrd').box

                for replica in range(self.number_of_replicas):

                    task = Task()
                    task.name = 'system:{}-replica:{}'.format(system, replica)

                    task.pre_exec = self.engine['pre_exec']
                    task.executable = self.engine['executable']['openmp_cuda']
                    task.arguments = self.engine['arguments']
                    task.mpi = self.engine['mpi']
                    task.cores = self.engine['cores'] or self.cores

                    task.arguments += ['esmacs-stage-{}.conf'.format(step)]

                    task.copy_input_data = ['$SHARED/esmacs-stage-{}.conf'.format(step)]

                    task.post_exec = ['echo {}-{} > simulation.desc'.format(stage.name, task.name)]

                    links = ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-cons.pdb'.format(system)]

                    settings = dict(BOX_X=box[0], BOX_Y=box[1], BOX_Z=box[2], SYSTEM=system,
                                    STEP=self.step_count[step], CUTOFF=self.cutoff, SWITCHING=self.cutoff-2.0,
                                    PAIRLISTDIST=self.cutoff+1.5, WATERMODEL=self.water_model,
                                    INPUT='', OUTPUT=stage.name)

                    if step > 0:
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.name, previous_stage.name,
                                                                       previous_task.name)
                        links += [path + previous_stage.name + suffix for suffix in ['.coor', '.xsc', '.vel']]
                        settings['INPUT'] = previous_stage.name
                    else:
                        links += ['$SHARED/{}-complex.pdb'.format(system)]

                    task.link_input_data = links

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
        f = 'default-configs/esmacs-stage-{}.conf'
        files = [resource_filename(__name__, f.format(step)) for step in range(self.numsteps)]
        for system in self.systems:
            comps = [self.rootdir] + system.split('-') + [system]
            base = os.path.join(*comps)
            files += [base+'-complex.pdb', base+'-complex.top', base+'-cons.pdb']
        return files

    @property
    def total_cores(self):
        return self.cores * self.number_of_replicas * len(self.systems)
