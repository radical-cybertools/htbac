import radical.utils as ru
from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


class Esmacs_MPI(object):
    
    '''
    esmacs protocol consists of 4 stages: 

    1) Minimization
    2) Equilibration step 1 (heating and restraint relaxation)
    3) Equilibration step 1 (300K unrestrained NPT)
    4) Production run
   
    shared_data will have provide access to folders inside rootdir:
        build, constraints, mineq_confs, MMPBSA, and sim_conf folders

    '''

    def __init__(self, replicas=0, rootdir=None, workflow=None):

        self._replicas   = replicas
        self.rootdir     = rootdir  # this will ensure that this instance only looks at its rootdir in shared_data
        self.executable  = ['/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-MPI-BlueWaters/namd2']

        #self.cpu_reqs    = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}
        self.cores       = 32
        self.workflow    = workflow
        
        #profiler for ESMACS PoE

        self._uid = ru.generate_id('radical.htbac.esmacs')
        self._logger = ru.get_logger('radical.htbac.esmacs')
        self._prof = ru.Profiler(name = self._uid) 
        self._prof.prof('create esmacs instance', uid=self._uid)


        self.my_list = list()

        for subdir, dirs, files in os.walk(self.rootdir):

            for file in files:
                self.my_list.append(os.path.join(subdir, file))

    @property
    def input_data(self):

        return self.rootdir

    @property
    def replicas(self):
        return self._replicas
    

    def generate_pipeline(self):

        # Create a single Pipeline

        p = Pipeline()

        # Create a new stage for every step in the workflow 

        s1 = Stage()
        s1_ref = dict()
        count = 0 
        print self.rootdir

        for replica in range(self._replicas):
            t = Task()
            t.name = "replica_{0}_step_{1}".format(replica,self.workflow[count]) 
            task_ref = "$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s1.uid, t.uid)
        
            t.copy_input_data = ["$SHARED/" + self.rootdir + ".tgz > " + self.rootdir + ".tgz"]

            
            t.pre_exec = ['tar zxvf {input1}'.format(input1=self.rootdir + ".tgz"), 
            "sed -i 's/REPX/{input2}/g' {input1}/*_confs/*.conf".format(input1 = self.rootdir, input2 = replica),
            'mkdir -p {input1}/replicas/rep{input2}/equilibration; touch {input1}/replicas/rep{input2}/equilibration/holder; mkdir -p {input1}/replicas/rep{input2}/simulation; touch {input1}/replicas/rep{input2}/simulation/holder'.format(
                                input1=self.rootdir, input2=replica)]
            

            # We create a list of all the NAMD flags required by the executable
            # and pass the path where the executable argument lies
            # and pass arg from pre-exec to the *.conf to replace REPX with the replica index

            t.arguments = ['%s/mineq_confs/eq0.conf' % self.rootdir]

            t.executable = self.executable 
            t.cores = self.cores
            s1_ref["replica_{0}_step_{1}".format(replica, self.workflow[count])] = task_ref
            s1.add_tasks(t)

        p.add_stages(s1)

        count += 1
        s2 = Stage()
        s2_ref = dict()

        for replica in range(self._replicas):
            t = Task()
            t.name = "replica_{0}_step_{1}".format(replica,self.workflow[count])
            task_ref = "$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s2.uid, t.uid)

            task_path = s1_ref["replica_{0}_step_{1}".format(replica, self.workflow[count-1])]

            
            #copy_input_data allows the current replica to stage output data from the same replica that were generated by a previous step

            t.copy_input_data = [task_path+'/replicas/rep{input1}/equilibration/{input2}.coor > {input3}/replicas/rep{input1}/equilibration/{input2}.coor'.format(input1 = replica, 
                                                 input2 = self.workflow[count-1], 
                                                 input3 = self.rootdir,
                                                 input4 = self.workflow[count]),
            task_path+'/replicas/rep{input1}/equilibration/{input2}.vel > {input3}/replicas/rep{input1}/equilibration/{input2}.vel'.format(input1 = replica,
                             input2 = self.workflow[count-1],
                             input3 = self.rootdir,
                             input4 = self.workflow[count]),
            task_path+'/replicas/rep{input1}/equilibration/{input2}.xsc > {input3}/replicas/rep{input1}/equilibration/{input2}.xsc'.format(input1 = replica,
                                    input2 = self.workflow[count-1],
                                    input3 = self.rootdir,
                                    input4 = self.workflow[count])]


            #this is the original root directory 
            for f in self.my_list:
                t.copy_input_data.append("{stage1}/".format(stage1=task_path) + f + " > " + f)

            t.executable = self.executable
            t.cores = self.cores

            #change the output in eq1 to have /_replicas/rep{input1}/equilibration/{input2}.coor
            t.arguments = ['+ppn','30','+pemap', '0-29', '+commap', '30', '%s/mineq_confs/eq1.conf' % self.rootdir]   

            #we obtain the task path of the previous step for current replica
            
                 
            s2_ref["replica_{0}_step_{1}".format(replica, self.workflow[count])] = task_ref
            s2.add_tasks(t)     

        p.add_stages(s2)

        count += 1

        s3 = Stage()
        s3_ref = dict()

        for replica in range(self._replicas):
            t = Task()
            t.name = "replica_{0}_step_{1}".format(replica,self.workflow[count])
            task_ref = "$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s3.uid, t.uid)

            t.executable = self.executable
            t.cores = self.cores

            #change the output in eq2 to have /_replicas/rep{input1}/eq/{input2}.coor
            t.arguments = ['+ppn','30','+pemap', '0-29', '+commap', '30', '%s/mineq_confs/eq2.conf' % self.rootdir]   

            #we obtain the task path of the previous step for current replica
            task_path = s2_ref["replica_{0}_step_{1}".format(replica, self.workflow[count-1])]
            

            # copy_input_data allows the current replica to stage output data from the same replica in a previous step

            t.copy_input_data = [task_path+'/replicas/rep{input1}/equilibration/{input2}.coor > {input3}/replicas/rep{input1}/equilibration/{input2}.coor'.format(input1 = replica, 
                                                 input2 = self.workflow[count-1], 
                                                 input3 = self.rootdir,
                                                 input4 = self.workflow[count]),
            task_path+'/replicas/rep{input1}/equilibration/{input2}.vel > {input3}/replicas/rep{input1}/equilibration/{input2}.vel'.format(input1 = replica,
                             input2 = self.workflow[count-1],
                             input3 = self.rootdir,
                             input4 = self.workflow[count]),
            task_path+'/replicas/rep{input1}/equilibration/{input2}.xsc > {input3}/replicas/rep{input1}/equilibration/{input2}.xsc'.format(input1 = replica,
                                    input2 = self.workflow[count-1],
                                    input3 = self.rootdir,
                                    input4 = self.workflow[count])]

            
            for f in self.my_list:
                t.copy_input_data.append("{stage2}/".format(stage2=task_path) + f + " > " + f)

            s3_ref["replica_{0}_step_{1}".format(replica, self.workflow[count])] = task_ref
            s3.add_tasks(t)  

        p.add_stages(s3)

        count += 1
        s4 = Stage()
        s4_ref = dict()

        for replica in range(self._replicas):
            t = Task()
            t.name = "replica_{0}_step_{1}".format(replica,self.workflow[count])
            task_ref = "$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s4.uid, t.uid)
            task_path = s3_ref["replica_{0}_step_{1}".format(replica, self.workflow[count-1])]
        


            # copy_input_data allows the current replica to stage output data from the same replica in a previous step

            t.copy_input_data = [task_path+'/replicas/rep{input1}/equilibration/{input2}.coor > {input3}/replicas/rep{input1}/equilibration/{input2}.coor'.format(input1 = replica, 
                                                 input2 = self.workflow[count-1], 
                                                 input3 = self.rootdir,
                                                 input4 = self.workflow[count]),
            task_path+'/replicas/rep{input1}/equilibration/{input2}.vel > {input3}/replicas/rep{input1}/equilibration/{input2}.vel'.format(input1 = replica,
                             input2 = self.workflow[count-1],
                             input3 = self.rootdir,
                             input4 = self.workflow[count]),
            task_path+'/replicas/rep{input1}/equilibration/{input2}.xsc > {input3}/replicas/rep{input1}/equilibration/{input2}.xsc'.format(input1 = replica,
                                    input2 = self.workflow[count-1],
                                    input3 = self.rootdir,
                                    input4 = self.workflow[count])]

            for f in self.my_list:
                t.copy_input_data.append("{stage3}/".format(stage3=task_path) + f + " > " + f)
            
            t.executable = self.executable
            t.cores = self.cores
            

            #change the output in eq1 to have /_replicas/rep{input1}/equilibration/{input2}.coor
            t.arguments = ['+ppn','30','+pemap', '0-29', '+commap', '30', '%s/sim_conf/sim1.conf' % self.rootdir]   
            
            #we obtain the task path of the previous step for current replica
            
            s4_ref["replica_{0}_step_{1}".format(replica, self.workflow[count])] = task_ref
            s4.add_tasks(t) 

        p.add_stages(s4)

        return p





