# Protocol class

import uuid
import pkg_resources

import parmed as pmd

import radical.utils as ru
from radical.entk import Pipeline, Stage, Task

# constants
_simulation_file_suffixes = ['.coor', '.xsc', '.vel']
_reduced_steps = dict(eq0=1000, eq1=5000, eq2=1000, sim1=50000)
_full_steps = dict(eq0=1000, eq1=30000, eq2=800000, sim1=2000000)
NAMD2 = '/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2'
NAMD_TI_ANALYSIS = "/u/sciteam/farkaspa/namd/ti/namd2_ti.pl"  


class Protocol(object):
    def __init__(self, 
            protocol = None, 
            replicas = 0, 
            systems = list(), 
            workflow = None, 
            cores = 0,
            full = False, 
            ligand = None,
            lambdas = 1, 
            additional=list(),
            **kwargs):

    self.protocol = protocol
    self.replicas = replicas
    self.systems = systems
    self.cores = cores
    self.step_count = _full_steps if full else _reduced_steps
    self.workflow = workflow or ['eq0', 'eq1', 'eq2', 'sim1']
    self.id = uuid.uuid1()  # generate id


    # Ties parameters
    # =================

    if self.protocol == 'Ties':

        self.lambdas = lambas 
        self.lambdas = np.linspace(0.0, 1.0, number_of_windows, endpoint=True)
        self.lambdas = np.append(self.lambdas, additional or [0.05, 0.95])
        self.ligand = '-ligands' if ligand else ''
        self.additional = additional # for additional adaptive quad windows 
       
        print "Lambda Windows: ", self.lambdas
        print "step count: ", self.step_count 

        # Input data
        @property
        def input_data(self):
            files = ['default_configs/ties-{}.conf'.format(step) for step in self.workflow]
            for system in self.systems:
                files += ['systems/ties{lig}/{s}/build/{s}-complex.pdb'.format(lig=self.ligand, s=system)]
                files += ['systems/ties{lig}/{s}/build/{s}-complex.top'.format(lig=self.ligand, s=system)]
                files += ['systems/ties{lig}/{s}/build/{s}-tags.pdb'.format(lig=self.ligand, s=system)]
            # print "Input files:", files
            return files

    # Esmacs parameters
    # =================

    if self.protocol == 'Esmacs':
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


    @property
    def replicas(self):
        return self.number_of_replicas*len(self.lambdas)*len(self.systems)



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


    def Ties(self):
        
        pipeline = Pipeline()

        # Simulation stages
        # =================

        for step in self.workflow:
            stage = Stage()
            stage.name = step
            print stage.name

            for system in self.systems:
                box = pmd.amber.AmberAsciiRestart('systems/ties{lig}/{s}/build/{s}-complex.crd'.format(lig=self.ligand, s=system)).box
                    
                for replica in range(self.number_of_replicas):
                    for ld in self.lambdas:
                    
                        task = Task()
                        task.name = 'system_{}_replica_{}_lambda_{}'.format(system, replica, ld)

                        task.copy_input_data = ['$SHARED/ties-{}.conf'.format(stage.name)]
                        task.pre_exec += ["sed -i 's/BOX_X/{}/g' *.conf".format(box[0]),
                                          "sed -i 's/BOX_Y/{}/g' *.conf".format(box[1]),
                                          "sed -i 's/BOX_Z/{}/g' *.conf".format(box[2]),
                                          "sed -i 's/SYSTEM/{}/g' *.conf".format(system)]

                        task.pre_exec += ["sed -i 's/STEP/{}/g' *.conf".format(self.step_count[step])]

                        task.pre_exec += ["sed -i 's/LAMBDA/{}/g' *.conf".format(ld)]

                        task.arguments += ['ties-{}.conf'.format(step)]
                        task.executable = ['NAMD2']         
                        task.mpi = True
                        task.cores = self.cores

                        links = []
                        links += ['$SHARED/{}-complex.top'.format(system), '$SHARED/{}-tags.pdb'.format(system)]
                        if self.workflow.index(step):
                            previous_stage = pipeline.stages[-1]
                            previous_task = next(t for t in previous_stage.tasks if t.name == task.name)
                            path = '$Pipeline_{}_Stage_{}_Task_{}/'.format(pipeline.uid, previous_stage.uid, previous_task.uid)
                            links += [path+previous_stage.name+suffix for suffix in _simulation_file_suffixes]
                        else:
                            links += ['$SHARED/{}-complex.pdb'.format(system)]

                        print "Linking files:", links
                        task.link_input_data = links

                        
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

            for p in filter(None, [pipeline, previous_pipeline]):
                production_stage = next(stage for stage in p.stages if stage.name == 'prod')
                production_tasks = [t for t in production_stage.tasks if analysis_task.name in t.name]
                links = ['$Pipeline_{}_Stage_{}_Task_{}/alch_{}_ti.out'.format(p.uid, production_stage.uid, t.uid, t.name.split('_lambda_')[-1]) for t in production_tasks]
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
        #average_task.download_output_data = ['dgs.out']  # .format(pipeline.uid)]

        average.add_tasks(average_task)
        pipeline.add_stages(average)


        print 'TIES pipeline has', len(pipeline.stages), 'stages. Tasks counts:', [len(s.tasks) for s in pipeline.stages]
        return pipeline
    

if self.protocol == 'esmacs':

    # self._uid = ru.generate_id('radical.htbac.protocol')
    # self._logger = ru.get_logger('radical.htbac.protocol')
    # self._prof = ru.Profiler(name=self._uid)
    # self._prof.prof('create protocol instance', uid=self._uid)
    
    Esmacs() 

if self.protocol = 'ties':


#     # self._uid = ru.generate_id('radical.htbac.protocol')
#     # self._logger = ru.get_logger('radical.htbac.protocol')
#     # self._prof = ru.Profiler(name=self._uid)
#     # self._prof.prof('create protocol instance', uid=self._uid)

     Ties()  




