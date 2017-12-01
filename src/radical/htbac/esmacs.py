import radical.utils as ru
from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os


class Esmacs(object):
    
    '''
    esmacs protocol consists of 7 stages: 

    1) Untar simulation tarball
    2) preprep
    3) Minimization
    4) Equilibration step 1 (heating and restraint relaxation)
    5) Equilibration step 1 (300K unrestrained NPT)
    6) Production run
    7) Create output tarball 
    '''


    def __init__(self, replicas=0, rootdir=None):

        self.replicas    = replicas
        self.rootdir     = rootdir
        self.executable  = ['/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2']
        self.pre_exec    = ['export OMP_NUM_THREADS=1']
        self.cpu_reqs    = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}
        
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

    def generate_pipeline(self):

        # Create a Pipeline object
        p = Pipeline()

        # ---------------------------------------------------------------------------
        # Stage 1

        s1 = Stage()

        # List of references to tasks in stage 1
        stage_1_ref = list()

        # Add tasks to stage 1
        for replica_ind in range(self.replicas):
            t1 = Task()
            t1.name = 'untar'
            t1.executable = ["/bin/bash"]
            t1.arguments = ['-l', '-c', 'tar zxvf {input1} -C ./'.format(input1=self.rootdir + ".tgz")]
            t1.cpu_reqs = self.cpu_reqs
            t1.pre_exec = self.pre_exec
            t1.copy_input_data = ["$SHARED/" + self.rootdir + ".tgz > " + self.rootdir + ".tgz"]

            stage_1_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s1.uid, t1.uid))

            s1.add_tasks(t1)

        p.add_stages(s1)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Stage 2

        s2 = Stage()

        # List of references to tasks in stage 2
        stage_2_ref = list()

        # Add tasks to stage 2
        for replica_ind in range(self.replicas):
            t2 = Task()
            t2.name = 'preprep'
            t2.executable = ["/bin/bash"]
            t2.arguments = ['-l', '-c',
                            'find -L {input1} -type f -print0 | xargs -0 sed -i \'s/REPX/{input2}/g\' ; mkdir -p {input1}/replicas/rep{input2}/equilibration; touch {input1}/replicas/rep{input2}/equilibration/holder; mkdir -p {input1}/replicas/rep{input2}/simulation; touch {input1}/replicas/rep{input2}/simulation/holder'.format(
                                input1=self.rootdir, input2=replica_ind)]
            t2.cpu_reqs = self.cpu_reqs
            t2.pre_exec = self.pre_exec
            t2.copy_input_data = []

            for f in self.my_list:
                t2.copy_input_data.append("{stage1}/".format(stage1=stage_1_ref[replica_ind]) + f + " > " + f)

            stage_2_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s2.uid, t2.uid))
            s2.add_tasks(t2)

        p.add_stages(s2)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Stage 3
        s3 = Stage()

        # List of references to tasks in stage 3
        stage_3_ref = list()

        # Add tasks to stage 3
        for replica_ind in range(self.replicas):
            t3 = Task()
            t3.name = 'stage3_namd'
            t3.executable = self.executable
            t3.cpu_reqs = self.cpu_reqs
            t3.pre_exec = self.pre_exec
            t3.arguments = ["%s/mineq_confs/eq0.conf" % self.rootdir]

            t3.copy_input_data = [
                '{stage2}/{input1}/replicas/rep{input2}/equilibration/holder > {input1}/replicas/rep{input2}/equilibration/holder'.format(
                    stage2=stage_2_ref[replica_ind], input1=self.rootdir, input2=replica_ind)]

            for f in self.my_list:
                t3.copy_input_data.append("{stage2}/".format(stage2=stage_2_ref[replica_ind]) + f + " > " + f)

            stage_3_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s3.uid, t3.uid))
            s3.add_tasks(t3)

        p.add_stages(s3)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Stage 4

        s4 = Stage()

        # List of references to tasks in stage 4
        stage_4_ref = list()

        # Add tasks to stage 4
        for replica_ind in range(self.replicas):
            t4 = Task()
            t4.name = 'stage4_namd'
            t4.executable = self.executable
            t4.arguments = ["%s/mineq_confs/eq1.conf" % self.rootdir]
            t4.cpu_reqs = self.cpu_reqs
            t4.pre_exec = self.pre_exec
            

            t4.copy_input_data = [
                '{stage3}/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(
                    stage3=stage_3_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage3}/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(
                    stage3=stage_3_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage3}/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(
                    stage3=stage_3_ref[replica_ind], input1=self.rootdir, input2=replica_ind)]

            for f in self.my_list:
                t4.copy_input_data.append("{stage3}/".format(stage3=stage_3_ref[replica_ind]) + f + " > " + f)

            stage_4_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s4.uid, t4.uid))
            s4.add_tasks(t4)

        p.add_stages(s4)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Stage 5

        s5 = Stage()

        # List of references to tasks in stage 5
        stage_5_ref = list()

        # Add tasks to stage 5

        for replica_ind in range(self.replicas):
            t5 = Task()
            t5.name = 'stage5_namd'
            t5.executable = self.executable
            t5.arguments = ["%s/mineq_confs/eq2.conf" % self.rootdir]
            t5.cpu_reqs = self.cpu_reqs
            t5.pre_exec = self.pre_exec                

            t5.copy_input_data = [
                '{stage4}/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(
                    stage4=stage_4_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage4}/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(
                    stage4=stage_4_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage4}/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(
                    stage4=stage_4_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage4}/{input1}/replicas/rep{input2}/equilibration/eq1.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(
                    stage4=stage_4_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage4}/{input1}/replicas/rep{input2}/equilibration/eq1.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(
                    stage4=stage_4_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage4}/{input1}/replicas/rep{input2}/equilibration/eq1.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(
                    stage4=stage_4_ref[replica_ind], input1=self.rootdir, input2=replica_ind)]

            for f in self.my_list:
                t5.copy_input_data.append("{stage4}/".format(stage4=stage_4_ref[replica_ind]) + f + " > " + f)

            stage_5_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s5.uid, t5.uid))
            s5.add_tasks(t5)

        p.add_stages(s5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Stage 6

        s6 = Stage()

        # List of references to tasks in stage 6
        stage_6_ref = list()

        # Add tasks to stage 6
        for replica_ind in range(self.replicas):
            t6 = Task()
            t6.name = 'stage6_namd'
            t6.executable = self.executable
            t6.arguments = ["%s/sim_confs/sim1.conf" % self.rootdir]
            t6.cpu_reqs = self.cpu_reqs
            t6.pre_exec = self.pre_exec

            t6.copy_input_data = [
                '{stage2}/{input1}/replicas/rep{input2}/simulation/holder > {input1}/replicas/rep{input2}/simulation/holder'.format(
                    stage2=stage_2_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq1.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq1.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq1.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq2.xsc > {input1}/replicas/rep{input2}/equilibration/eq2.xsc'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq2.vel > {input1}/replicas/rep{input2}/equilibration/eq2.vel'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage5}/{input1}/replicas/rep{input2}/equilibration/eq2.coor > {input1}/replicas/rep{input2}/equilibration/eq2.coor'.format(
                    stage5=stage_5_ref[replica_ind], input1=self.rootdir, input2=replica_ind)]

            for f in self.my_list:
                t6.copy_input_data.append("{stage5}/".format(stage5=stage_5_ref[replica_ind]) + f + " > " + f)

            stage_6_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s6.uid, t6.uid))
            s6.add_tasks(t6)

        p.add_stages(s6)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Stage 7

        s7 = Stage()

        # List of references to tasks in stage 7
        stage_7_ref = list()

        # Add tasks to stage 7
        for replica_ind in range(self.replicas):
            t7 = Task()
            t7.name = 'stage7_tar'
            t7.executable = ["/bin/bash"]
            t7.arguments = ['-l', '-c',
                            'tar -hczf {input1}.tgz -C {input2}/replicas .'.format(input1='rep%s' % replica_ind,
                                                                                   input2=self.rootdir)]
            t7.cpu_reqs = self.cpu_reqs
            t7.pre_exec = self.pre_exec
            t7.copy_input_data = [
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq0.coor > {input1}/replicas/rep{input2}/equilibration/eq0.coor'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq0.xsc > {input1}/replicas/rep{input2}/equilibration/eq0.xsc'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq0.vel > {input1}/replicas/rep{input2}/equilibration/eq0.vel'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq1.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq1.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq1.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq2.xsc > {input1}/replicas/rep{input2}/equilibration/eq1.xsc'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq2.vel > {input1}/replicas/rep{input2}/equilibration/eq1.vel'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/equilibration/eq2.coor > {input1}/replicas/rep{input2}/equilibration/eq1.coor'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/simulation/sim1.xsc > {input1}/replicas/rep{input2}/simulation/sim1.xsc'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/simulation/sim1.vel > {input1}/replicas/rep{input2}/simulation/sim1.vel'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind),
                '{stage6}/{input1}/replicas/rep{input2}/simulation/sim1.coor > {input1}/replicas/rep{input2}/simulation/sim1.coor'.format(
                    stage6=stage_6_ref[replica_ind], input1=self.rootdir, input2=replica_ind)]

            t7.download_output_data = ["rep{0}.tgz".format(replica_ind)]
            s7.add_tasks(t7)

        p.add_stages(s7)

            # ---------------------------------------------------------------------------

        return p
