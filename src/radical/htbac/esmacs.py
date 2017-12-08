import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_MMPBSA_ANALYSIS = "WHERE IS IT?"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(eq0=1000, eq1=30000, eq2=92000, sim1=200000)
_full_steps = dict(eq0=1000, eq1=30000, eq2=970000, sim1=2000000)


class Esmacs(object):
    def __init__(self, number_of_replicas, system, workflow, full=False):

        self.number_of_replicas = number_of_replicas
        self.system = system
        self.box = pmd.amber.AmberAsciiRestart('systems/esmacs/{s}/build/{s}-complex.crd'.format(s=system)).box
        self.step_count = _full_steps if full else _reduced_steps

        self.workflow = workflow
        
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

            for replica in range(self.number_of_replicas):

                task = Task()
                task.name = 'replica_{}'.format(replica)

                task.arguments += ['esmacs-{}.conf'.format(stage.name)]
                task.copy_input_data = ['$SHARED/esmacs-{}.conf'.format(stage.name)]
                task.executable = [NAMD2]

                task.mpi = True
                task.cores = 32

                links = []
                links += ['$SHARED/{}-complex.top'.format(self.system), '$SHARED/{}-cons.pdb'.format(self.system)]

                if self.workflow.index(step):
                    previous_stage = pipeline.stages[-1]
                    previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                    path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid,
                                                                   previous_task.uid)
                    links += [path + previous_stage.name + suffix for suffix in _simulation_file_suffixes]
                else:
                    links += ['$SHARED/{}-complex.pdb'.format(self.system)]

                task.link_input_data = links

                task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.box[0]),
                                  "sed -i 's/BOX_Y/{}/g' *.conf".format(self.box[1]),
                                  "sed -i 's/BOX_Z/{}/g' *.conf".format(self.box[2]),
                                  "sed -i 's/SYSTEM/{}/g' *.conf".format(self.system)]

                task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[step])]

                stage.add_tasks(task)

            pipeline.add_stages(stage)

        print 'ESM pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = []
        files += ['default_configs/esmacs-{}.conf'.format(step) for step in self.workflow]
        files += ['systems/esmacs/{s}/build/{s}-complex.pdb'.format(s=self.system)]
        files += ['systems/esmacs/{s}/build/{s}-complex.top'.format(s=self.system)]
        files += ['systems/esmacs/{s}/constraint/{s}-cons.pdb'.format(s=self.system)]
        return files

    @property
    def replicas(self):
        return self.number_of_replicas
