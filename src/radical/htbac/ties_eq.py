import numpy as np
import parmed as pmd
import uuid

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task


NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(min=1000, eq1=5000, eq2=10000)
_full_steps = dict(min=1000, eq1=30000, eq2=970000)



class TiesEquilibration(object):

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

        self.workflow = workflow or ['min', 'eq1', 'eq2']
        
        # Profiler for TIES PoE

        self._uid = ru.generate_id('radical.htbac.ties')
        self._logger = ru.get_logger('radical.htbac.ties')
        self._prof = ru.Profiler(name=self._uid)
        self._prof.prof('create ties instance', uid=self._uid)

    def id(self):
        return self._id

    # Generate a new pipeline
    def generate_pipeline(self):

        pipeline = Pipeline()

        pipeline.name = '_'.join(str(l) for l in self.lambdas)

        # Simulation stages
        # =================
        for step in self.workflow:
            stage = Stage()
            stage.name = step

            for replica in range(self.number_of_replicas):
                for ld in self.lambdas:
                    
                    task = Task()
                    task.name = 'replica_{}_lambda_{}'.format(replica, ld)

                    task.arguments += ['ties-{}.conf'.format(stage.name)]
                    task.copy_input_data = ['$SHARED/ties-{}.conf'.format(stage.name)]
                    task.executable = [NAMD2]

                    task.mpi = True
                    task.cores = self.cores

                    links = []
                    links += ['$SHARED/{}-complex.top'.format(self.system), '$SHARED/{}-tags.pdb'.format(self.system)]

                    if self.workflow.index(step):
                        previous_stage = pipeline.stages[-1]
                        previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                        path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid, previous_task.uid)
                        links += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
                    else:
                        links += ['$SHARED/{}-complex.pdb'.format(self.system)]

                    task.link_input_data = links

                    task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(self.box[0]),
                                      "sed -i 's/BOX_Y/{}/g' *.conf".format(self.box[1]),
                                      "sed -i 's/BOX_Z/{}/g' *.conf".format(self.box[2]),
                                      "sed -i 's/SYSTEM/{}/g' *.conf".format(self.system)]

                    task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[step])]

                    task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

                    stage.add_tasks(task)

            pipeline.add_stages(stage)

        print 'TIES equilibration pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]

        return pipeline

    # Input data
    @property
    def input_data(self):
        files = []
        files += ['adaptive_configs/ties-{}.conf'.format(step) for step in ['min', 'eq1', 'eq2', 'prod']]
        files += ['systems/ties{lig}/{s}/build/{s}-complex.pdb'.format(lig=self.ligand, s=self.system)]
        files += ['systems/ties{lig}/{s}/build/{s}-complex.top'.format(lig=self.ligand, s=self.system)]
        files += ['systems/ties{lig}/{s}/build/{s}-tags.pdb'.format(lig=self.ligand, s=self.system)]
        return files

    @property
    def replicas(self):
        return self.number_of_replicas*len(self.lambdas)