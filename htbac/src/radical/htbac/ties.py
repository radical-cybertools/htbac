from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os
import traceback
# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


class NamdTask(Task):
    def __init__(self, name):
        super(NamdTask, self).__init__()
        self.name = name
        self.executable = ['/u/sciteam/jphillip/NAMD_LATEST_CRAY-XE-ugni-smp-BlueWaters/namd2']
        #self.cores = cores
        self.pre_exec = ['export OMP_NUM_THREADS=1']
        self.cpu_reqs = {'processes': 1, 'process_type': 'MPI', 'threads_per_process': 31, 'thread_type': None}
        #self.mpi = mpi


if __name__ == '__main__':
    # Set up parameters

    rootdir = 'bace1_b01'
    my_list = []
        
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            #print os.path.join(subdir, file)
            my_list.append(os.path.join(subdir, file))

    cores_per_pipeline = 32
    pipelines = set()
    #stage_ref = []
    replicas = 5
    lambdas  = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    workflow = ['min', 'eq1', 'eq2', 'prod']


    # Generate pipelines

    for replica in range(replicas):
        for ld in lambdas:
            p = Pipeline()
            stage_ref = []
            for step in workflow:

                task_ref = []
                #s, t = Stage(), NamdTask(name=step, cores=cores_per_pipeline)
                s, t = Stage(), NamdTask(name=step)
                t.arguments = ['+ppn','30','+pemap', '0-29', '+commap', '30','replica_{}/lambda_{}/{}.conf'.format(replica, ld, step), '&>', 'replica_{}/lambda_{}/{}.log'.format(replica, ld, step)]
                task_ref.append("$Pipeline_{0}_Stage_{1}_Task_{2}/".format(p.uid, s.uid, t.uid))
                #print task_ref
                s.add_tasks(t)
                for task_paths in stage_ref:
                    for task_path in task_paths:
                        #print task_path 
                        #print count 
                        #print workflow[stage_ref.index(task_paths)]
                        t.copy_input_data.append(task_path+'replica_{0}/lambda_{1}/{2}.coor'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                        t.copy_input_data.append(task_path+'replica_{0}/lambda_{1}/{2}.xsc'.format(replica,ld,workflow[stage_ref.index(task_paths)]))
                        t.copy_input_data.append(task_path+'replica_{0}/lambda_{1}/{2}.vel'.format(replica,ld,workflow[stage_ref.index(task_paths)]))

                print t.copy_input_data

                for f in my_list:
                    t.copy_input_data.append("{}/".format(replica)+f+" > "+f)
            

            	stage_ref.append(task_ref)
                #print stage_ref
                #print count

                p.add_stages(s)

            pipelines.add(p)


    # Resource and AppManager

    res_dict = {
        'resource': 'ncsa.bw_aprun',
        'walltime': 1440,
        'cores': replicas * len(lambdas) * cores_per_pipeline,
        'project': 'bamm',
        'queue': 'high',
        'access_schema': 'gsissh'}

    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)

    # FIXME this is not going to work. `rootdir` has to be copied over, but
    # only once. If `rootdir` is tarred up, then you have to untar it at then
    # other end. Where would you put that 1 untaring proccess?
    rman.shared_data = [rootdir]

    # Create Application Manager
    appman = AppManager(port=32775)

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(pipelines)

    # Run the Application Manager
    #appman.run()
