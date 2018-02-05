import uuid
import numpy as np
import pandas as pd
from StringIO import StringIO


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
            links = ['$Pipeline_{}_Stage_{}_Task_{}/alch_{}_{}_{}_ti.out'.format(previous_pipeline.uid, production_stage.uid, t.uid, t.name.split('_')[1], t.name.split('_')[3], production_stage.name) for t in production_tasks]
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


class AdaptiveQuadrature(object):
    def __init__(self, namd_ti, tol=2):
        self.namd_ti = namd_ti
        self.tol = tol
        self._process_data()

    splits = ['Partition 1 electrostatics',
              'Partition 1 vdW',
              'Partition 2 electrostatics']

    def _process_data(self):
        with open(self.namd_ti) as f:
            data = f.read()
            dfs = list()

            for s in self.splits:
                sp = data.split(s)
                dfs += [pd.read_csv(StringIO(sp[0].replace('\t', ' ')), delim_whitespace=True, usecols=[0, 1])]
                data = sp[1]

            self.p1v = dfs[2]

    def requested_windows(self):
        number_to_add = len(self.p1v)

        while True:
            newp1v = self.p1v.copy(deep=True)

            for index in range(len(self.p1v) - 1):
                dif = abs(self.p1v.loc[index]['dE/dl'] - self.p1v.loc[index + 1]['dE/dl'])
                if dif > self.tol:
                    newld = (self.p1v.loc[index]['Lambda'] + self.p1v.loc[index + 1]['Lambda']) / 2
                    print 'Add new ld at:', newld
                    newp1v.loc[len(newp1v)] = [newld, max(self.p1v.loc[index]['dE/dl'], self.p1v.loc[index + 1]['dE/dl'])]
                    number_to_add -= 1

                    if number_to_add == 0:
                        break

            newp1v.sort_values('Lambda', inplace=True)
            newp1v.reset_index(drop=True, inplace=True)
            self.p1v = newp1v

            if number_to_add == 0:
                break

        return self.p1v['Lambda'].as_matrix()
