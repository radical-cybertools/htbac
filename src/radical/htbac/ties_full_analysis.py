import uuid
import numpy as np

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task

NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"


class TiesAnalysis(object):
    def __init__(self, number_of_replicas, lambda_windows):
        self.number_of_replicas = number_of_replicas
        self.lambda_windows = lambda_windows
        self._id = uuid.uuid1()  # generate id

    def id(self):
        return self._id

    def generate_pipeline(self, previous_pipeline=None):
        pipeline = Pipeline()

        # Analysis stage
        # ==============
        # For every replica, calculate the dG value.
        analysis = Stage()
        analysis.name = 'analysis'

        for replica in range(self.number_of_replicas):
            analysis_task = Task()
            analysis_task.name = 'replica_{}'.format(replica)

            analysis_task.arguments += ['-d', '*ti.out', '>', 'dg_{}.out'.format(analysis_task.name)]
            analysis_task.executable = [NAMD_TI_ANALYSIS]

            analysis_task.mpi = False
            analysis_task.cores = 1

            production_stage = previous_pipeline.stages[0]  # The pipeline's first stage is the production run.
            production_tasks = [t for t in production_stage.tasks if analysis_task.name in t.name]
            links = ['$Pipeline_{}_Stage_{}_Task_{}/alch_{}_{}_ti.out'.format(previous_pipeline.uid, production_stage.uid, t.uid, t.name.split('_lambda_')[-1], production_stage.name) for t in production_tasks]
            analysis_task.link_input_data += links

            analysis.add_tasks(analysis_task)

        pipeline.add_stages(analysis)

        # Averaging stage
        # ===============
        average = Stage()
        average.name = 'average'

        average_task = Task()
        average_task.name = 'average_dg'
        average_task.arguments = ['-1 --quiet dg_* > dgs.out']  # .format(pipeline.uid)]
        average_task.executable = ['head']

        average_task.mpi = False
        average_task.cores = 1

        previous_stage = pipeline.stages[-1]
        previous_tasks = previous_stage.tasks

        links = ['$Pipeline_{}_Stage_{}_Task_{}/dg_{}.out'.format(pipeline.uid, previous_stage.uid, t.uid,
                                                                  t.name) for t in previous_tasks]
        average_task.link_input_data = links
        # average_task.download_output_data = ['dgs.out']  # .format(pipeline.uid)]

        average.add_tasks(average_task)
        pipeline.add_stages(average)

        return pipeline

