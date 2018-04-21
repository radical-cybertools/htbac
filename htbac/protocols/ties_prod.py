import numpy as np
import parmed as pmd
import uuid

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(prod=1000)
_full_steps = dict(prod=500000)


class TiesProduction(object):
    def __init__(self, number_of_replicas, number_of_windows=0, additional=list(),
                 system=None, workflow=None, cores=64, ligand=False, full=True):

        self.number_of_replicas = number_of_replicas
        self.lambdas = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        self.lambdas = np.append(self.lambdas, additional)
        self.ligand = '-ligands' if ligand else ''
        self.step_count = _full_steps if full else _reduced_steps

        self.system = system
        self.box = pmd.amber.AmberAsciiRestart('systems/ties{lig}/{s}/build/{s}-complex.crd'.format(lig=self.ligand, s=system)).box
        self.cores = cores
        self._id = uuid.uuid1()  # generate id

        self.workflow = workflow or 'prod'
        
        # Profiler for TIES PoE

        self._uid = ru.generate_id('radical.htbac.ties')
        self._logger = ru.get_logger('radical.htbac.ties')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create ties instance', uid=self._uid)

    def id(self):
        return self._id

    # Generate a new pipeline
    def generate_pipeline(self, previous_pipeline=None):

        pipeline = Pipeline()

        pipeline.name = '_'.join(str(l) for l in self.lambdas)

        # Production stage
        # =================
        stage = Stage()
        stage.name = self.workflow + '.' + pipeline.uid.split('.')[-1]  # Will this work?

        for replica in range(self.number_of_replicas):
            for ld in self.lambdas:

                task = Task()
                task.name = 'replica_{}_lambda_{}'.format(replica, ld)

                task.arguments += ['ties-{}.conf'.format(self.workflow)]
                task.copy_input_data = ['$SHARED/ties-{}.conf'.format(self.workflow)]
                task.executable = [NAMD2]

                task.mpi = True
                task.cores = self.cores

                links = []
                links += ['$SHARED/{}-complex.top'.format(self.system), '$SHARED/{}-tags.pdb'.format(self.system)]

                previous_stage = next(stage for stage in previous_pipeline.stages if stage.name in ['eq2', 'prod.{}'.format(previous_pipeline.uid.split('.')[-1])])
                previous_lambdas = np.array(previous_pipeline.name.split('_'), dtype=np.float)

                closest_lambda = previous_lambdas[(np.abs(previous_lambdas-ld)).argmin()]
                closest_task_name = 'replica_{}_lambda_{}'.format(replica, closest_lambda)

                previous_task = next(t for t in previous_stage.tasks if t.name == closest_task_name)
                path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(previous_pipeline.uid, previous_stage.uid, previous_task.uid)
                links += [path + previous_stage.name + suffix for suffix in _simulation_file_suffixes]

                task.link_input_data = links

                task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.box[0]),
                                  "sed -i 's/BOX_Y/{}/g' *.conf".format(self.box[1]),
                                  "sed -i 's/BOX_Z/{}/g' *.conf".format(self.box[2]),
                                  "sed -i 's/SYSTEM/{}/g' *.conf".format(self.system)]

                task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[self.workflow])]

                task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]
                task.pre_exec += ["sed -i 's/REPLICA/{}/g' *.conf".format(replica)]

                task.pre_exec += ["sed -i 's/INPUT/{}/g' *.conf".format(previous_stage.name)]
                task.pre_exec += ["sed -i 's/OUTPUT/{}/g' *.conf".format(stage.name)]

                stage.add_tasks(task)

        pipeline.add_stages(stage)

        # Analysis stage
        # ==============
        # Calculate the dU/dl value at each lambda window
        analysis = Stage()
        analysis.name = 'analysis'

        analysis_task = Task()
        analysis_task.name = 'analysis'

        analysis_task.arguments += ['-f', '>', 'dg.out']
        analysis_task.executable = [NAMD_TI_ANALYSIS]

        analysis_task.mpi = False
        analysis_task.cores = 1

        production_stage = pipeline.stages[-1]
        production_tasks = production_stage.tasks
        links = ['$Pipeline_{}_Stage_{}_Task_{}/alch_{}_{}_{}_ti.out'.format(pipeline.uid, production_stage.uid, t.uid, t.name.split('_')[1], t.name.split('_')[3], stage.name) for t in production_tasks]
        analysis_task.link_input_data += links

        analysis_task.download_output_data = ['dg.out > dg_{}.out'.format(self._id)]

        analysis.add_tasks(analysis_task)

        pipeline.add_stages(analysis)

        print 'TIES Production pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = []
        files += ['adaptive_configs/ties-{}.conf'.format(step) for step in self.workflow]
        files += ['systems/ties{lig}/{s}/build/{s}-complex.pdb'.format(lig=self.ligand, s=self.system)]
        files += ['systems/ties{lig}/{s}/build/{s}-complex.top'.format(lig=self.ligand, s=self.system)]
        files += ['systems/ties{lig}/{s}/build/{s}-tags.pdb'.format(lig=self.ligand, s=self.system)]
        return files

    @property
    def replicas(self):
        return self.number_of_replicas*len(self.lambdas)
