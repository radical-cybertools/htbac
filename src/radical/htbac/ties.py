import radical.utils as ru
from radical.entk import task
from radical.entk import stages
from radical.entk import pipeline
from radical.entk import appman
import os


class ties(object):

   # class NamdTask(Task):

    def __init__(self, replicas, lambda_initial, lambda_final, lambda_delta, rootdir, workflow):


        self.name             = esmacs
        self.replicas         = replicas
        self.lambda_initial   = lambda_initial
        self.lambda_final     = lambda_final
        self.lambda_delta     = lambda_delta
        self.rootdir          = rootdir
        self.executable       = ['/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2']
        self.pre_exec         = ['export OMP_NUM_THREADS=1']
        self.cpu_reqs         = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}
        self.workflow         = workflow

        my_list = []
            
        for subdir, dirs, files in os.walk(self.rootdir):
            for file in files:
                #print os.path.join(subdir, file)
                my_list.append(os.path.join(subdir, file))

        cores_per_pipeline = 32
        pipelines = set()
        #lambdas  = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
        workflow = ['min', 'eq1', 'eq2', 'prod']



        lambdas = [i/100.0 for i in range(self.lambda_initial, self.lambda_final, self.lambda_delta)]

        # Generate pipelines

        def generate_pipelines(self):

            for replica in range(self.replicas):
                for ld in lambdas:
                    p = Pipeline()
                    stage_ref = []
                    for step in workflow:

                        task_ref = []
                        s = Stage()
                        t = Task()
                        t.name = step 
                        t.executable = self.executable
                        t.pre_exec   = self.pre_exec
                        t.cpu_reqs   = self.cpu_reqs
                        t.arguments  = ['+ppn','30','+pemap', '0-29', '+commap', '30','replica_{}/lambda_{}/{}.conf'.format(replica, ld, step), '&>', 'replica_{}/lambda_{}/{}.log'.format(replica, ld, step)]
                        task_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid))
                        s.add_tasks(t)
                        for task_paths in stage_ref:
                            for task_path in task_paths:
                                t.copy_input_data.append(task_path+'replica_{0}/lambda_{1}/{2}.coor'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                                t.copy_input_data.append(task_path+'replica_{0}/lambda_{1}/{2}.xsc'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                                t.copy_input_data.append(task_path+'replica_{0}/lambda_{1}/{2}.vel'.format(replica,ld,workflow[stage_ref.index(task_paths)]))

                        print t.copy_input_data

                        for f in my_list:
                            t.copy_input_data.append("{}/".format(replica)+f+" > "+f)
                    
                    	stage_ref.append(task_ref)
                        
                        p.add_stages(s)

                    pipelines.add(p)

            return pipelines 


        
