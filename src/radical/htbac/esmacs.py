import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_MMPBSA_ANALYSIS = "WHERE IS IT?"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']


class Esmacs(object):
    def __init__(self, number_of_replicas, system, workflow):

        self.number_of_replicas = number_of_replicas
        self.system = system
        self.box = pmd.amber.AmberAsciiRestart('systems/esmacs/{}/build/complex.crd'.format(system)).box

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

                task.arguments += ['{}.conf'.format(stage.name)]
                task.copy_input_data = ['$SHARED/{}.conf'.format(stage.name)]
                task.executable = [NAMD2]

                task.mpi = True
                task.cores = 32

                links = []
                links += ['$SHARED/complex.top', '$SHARED/cons.pdb']

                if self.workflow.index(step):
                    previous_stage = pipeline.stages[-1]
                    previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                    path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid,
                                                                   previous_task.uid)
                    links += [path + previous_stage.name + suffix for suffix in _simulation_file_suffixes]
                else:
                    links += ['$SHARED/complex.pdb']

                task.link_input_data = links

                task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.box[0]),
                                  "sed -i 's/BOX_Y/{}/g' *.conf".format(self.box[1]),
                                  "sed -i 's/BOX_Z/{}/g' *.conf".format(self.box[2])]

                stage.add_tasks(task)

            pipeline.add_stages(stage)

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = []
        files += ['default_configs/esmacs/{}.conf'.format(step) for step in self.workflow]
        files += ['systems/esmacs/{}/build/{}'.format(self.system, desc) for desc in ['complex.pdb', 'complex.top']]
        files += ['systems/esmacs/{}/constraint/cons.pdb'.format(self.system)]
        return files

    @property
    def replicas(self):
        return self.number_of_replicas
