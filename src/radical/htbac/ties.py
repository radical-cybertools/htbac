import radical.utils as ru
from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os


class Ties(object):

   # class NamdTask(Task):

    def __init__(self, replicas = 0, lambda_initial = 0, lambda_final = 0, lambda_delta = 0, rootdir = None, workflow = None):

        self.replicas         = replicas
        self.lambda_initial   = lambda_initial
        self.lambda_final     = lambda_final*100
        self.lambda_delta     = int(lambda_delta*100)
        self.rootdir          = rootdir
        self.executable       = ['/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2']
        self.pre_exec         = ['export OMP_NUM_THREADS=1']
        self.cpu_reqs         = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}
        self.workflow         = workflow

        #profiler for TIES PoE

        self._uid = ru.generate_id('radical.htbac.ties')
        self._logger = ru.get_logger('radical.htbac.ties')
        self._prof = ru.Profiler(name = self._uid) 
        self._prof.prof('create ties instance', uid=self._uid)

        self.my_list = list()
            
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                #print os.path.join(subdir, file)
                self.my_list.append(os.path.join(subdir, file))

        self.lambdas = list()
        self.lambdas = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
        #workflow = ['min', 'eq1', 'eq2', 'prod']
        
        #self.lambdas = [i/100.0 for i in range(self.lambda_initial, self.lambda_final*100, self.lambda_delta*100)]



    @property
    def input_data(self):

        return self.rootdir

    # Generate pipelines
    def generate_pipeline(self):


    # Here we create 1 pipeline with n_stages where n is the number of steps in the workflow
    # In each stage we generate x_tasks where x is the lambdas* replicas

        p = Pipeline()
        stage_ref = dict()

        for index, step in enumerate(self.workflow):
            s = Stage()
            for replica in range(self.replicas):
                for ld in self.lambdas:
                    
                    
                    if index == 0:

                        t = Task()
                        t.name = "replica_{0}_lambda_{1}_step_{2}".format(replica,ld,step) 
                        self.pre_exec.append('tar zxvf {input1}'.format(input1=self.rootdir + ".tgz")) 
                        t.pre_exec = self.pre_exec
                        t.copy_input_data = ["$SHARED/" + self.rootdir + ".tgz > " + self.rootdir + ".tgz"]
                        t.executable = self.executable
                        t.arguments  = ['+ppn','30','+pemap', '0-29', '+commap', '30',
                                    'replica_{}/lambda_{}/{}.conf'.format(replica, ld, step), 
                                    '&>', 
                                    'replica_{}/lambda_{}/{}.log'.format(replica, ld, step)]

                        # obtain the task path of the previous step for current replica+lambda combination for any stage after stage 1 
                    
                        #task_ref = ["$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid)]
                        stage_ref["replica_{0}_lambda_{1}_step_{2}".format(replica,ld,step)]="$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid)

                        s.add_tasks(t)


                    if index != 0: 


                        t = Task()
                        t.name = "replica_{0}_lambda_{1}_step_{2}".format(replica,ld,step) 

                        #obtain task_path of current replica from previous workflow step 
                        task_path = stage_ref["replica_{0}_lambda_{1}_step_{2}".format(replica,ld,self.workflow[index-1])]
                        
                        t.copy_input_data =[task_path+'replica_{input1}/lambda_{input2}/{input3}.xsc > replica_{input1}/lambda_{input2}/{input3}.xsc'.format(input1 = replica, 
                                                     input2 = ld, 
                                                     input3 = self.workflow[index-1]),
                                            task_path+'replica_{input1}/lambda_{input2}/{input3}.vel > replica_{input1}/lambda_{input2}/{input3}.vel'.format(input1 = replica, 
                                                     input2 = ld, 
                                                     input3 = self.workflow[index-1])]

                        for f in self.my_list:
                            t.copy_input_data.append("{stage}/".format(stage=task_path) + f + " > " + f)


                        t.pre_exec   = self.pre_exec
                        t.executable = self.executable
                        t.cpu_reqs   = self.cpu_reqs
                        t.arguments  = ['+ppn','30','+pemap', '0-29', '+commap', '30',
                                        'replica_{}/lambda_{}/{}.conf'.format(replica, ld, step), 
                                        '&>', 
                                        'replica_{}/lambda_{}/{}.log'.format(replica, ld, step)]

                        # obtain the task path of the previous step for current replica+lambda combination for any stage after stage 1 
                        
                        #task_ref = ["$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid)]
                        stage_ref["replica_{0}_lambda_{1}_step_{2}".format(replica,ld,step)]="$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid)
                        s.add_tasks(t)
                
            p.add_stages(s)
        return p


        
