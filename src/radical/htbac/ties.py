import numpy as np
import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']


class Ties(object):
    def __init__(self, number_of_replicas, number_of_windows, system, workflow):

        self.number_of_replicas = number_of_replicas
        self.lambdas = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        self.system = system
        self.box = pmd.amber.AmberAsciiRestart('ties/{}/build/complex.crd'.format(system)).box

        self.workflow = workflow

        # Profiler for TIES PoE

        self._uid = ru.generate_id('radical.htbac.ties')
        self._logger = ru.get_logger('radical.htbac.ties')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create ties instance', uid=self._uid)

    # Generate a new pipeline
    def generate_pipeline(self):

        pipeline = Pipeline()

        # Simulation stages
        # =================
        for step in self.workflow:
            stage = Stage()
            stage.name = step

            for replica in range(self.number_of_replicas):
                for ld in self.lambdas:
                    
                    task = Task()
                    task.name = 'replica_{}_lambda_{}'.format(replica, ld)

                    task.arguments += ['{}.conf'.format(stage.name)]
                    task.copy_input_data = ['$SHARED/{}.conf'.format(stage.name)]
                    task.executable = [NAMD2]

                    task.mpi = True
                    task.cores = 32

                    links = []
                    links += ['$SHARED/complex.top', '$SHARED/tags.pdb']

                    if self.workflow.index(step):
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid, previous_task.uid)
                        links += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
                    else:
                        links += ['$SHARED/complex.pdb']

                    task.link_input_data = links

                    task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.box[0]),
                                      "sed -i 's/BOX_Y/{}/g' *.conf".format(self.box[1]),
                                      "sed -i 's/BOX_Z/{}/g' *.conf".format(self.box[2])]

                    task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

                    stage.add_tasks(task)

            pipeline.add_stages(stage)

        # Analysis stage
        # ==============
        analysis = Stage()
        analysis.name = 'analysis'

        for replica in range(self.number_of_replicas):
            analysis_task = Task()
            analysis_task.name = 'replica_{}'.format(replica)

            analysis_task.arguments += ['-d', '*ti.out', '>', 'dg_{}.out'.format(analysis_task.name)]
            analysis_task.executable = [NAMD_TI_ANALYSIS]

            analysis_task.mpi = False
            analysis_task.cores = 1

            production_stage = pipeline.stages[-1]
            production_tasks = [t for t in production_stage.tasks if analysis_task.name in t.name]
            links = ['$Pipeline_{}_Stage_{}_Task_{}/alch_{}_ti.out'.format(pipeline.uid, production_stage.uid, t.uid, t.name.split('_lambda_')[-1]) for t in production_tasks]
            analysis_task.link_input_data = links

            analysis.add_tasks(analysis_task)

        pipeline.add_stages(analysis)

        # # Averaging stage
        # # ===============
        # average = Stage()
        # average.name = 'average'
        #
        # average_task = Task()
        # average_task.name = 'average_dg'
        # # Change this to the actual averaging. How? Does the python come with np?
        # average_task.arguments = ['average']
        # average_task.executable = ['echo']
        #
        # average_task.mpi = False
        # average_task.cores = 1
        #
        # previous_stage = pipeline.stages[-1]
        # previous_tasks = previous_stage.tasks
        #
        # links = ['$Pipeline_{}_Stage_{}_Task_{}/dg_{}.out'.format(pipeline.uid, previous_stage.uid, t.uid,
        #                                                           t.name) for t in previous_tasks]
        # average_task._link_input_data = links
        #
        # average.add_tasks(average_task)
        # pipeline.add_stages(average)

        print 'Pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages],

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = []
        files += ['default_configs/ties/{}.conf'.format(step) for step in self.workflow]
        files += ['ties/{}/build/{}'.format(self.system, desc) for desc in ['complex.pdb', 'complex.top', 'tags.pdb']]
        return files

    @property
    def replicas(self):
        return self.number_of_replicas*len(self.lambdas)
