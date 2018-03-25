from radical.entk import Pipeline, Stage, Task, AppManager, ResourceManager
import os

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


def generate_pipeline():
    
    # Create a Pipeline object
    p = Pipeline()
    p.name = 'p1'

    # Create a Stage object 
    s1 = Stage()
    s1.name = 's1'

    # Create a Task object which creates a file named 'output.txt' of size 1 MB
    task = Task()  
    task.name = 't1' 
    task.pre_exec = ['export PATH="/lustre/atlas/scratch/farkaspall/chm126/miniconda3/bin:$PATH"',
                    'export HOME=/lustre/atlas/scratch/farkaspall/chm126',
                    'export MINICONDA3="$HOME/miniconda3"',
                    'export PATH="$MINICONDA3/bin:$PATH"',
                    'export LD_LIBRARY_PATH=$MINICONDA3/lib:$LD_LIBRARY_PATH']
     
    task.mpi = False 
    task.cores = 16
    task.executable = ['benchmark.py']
    task.argument = ['python -m']

    # Add the Task to the Stage
    s1.add_tasks(task)

    # Add Stage to the Pipeline
    p.add_stages(s1)

    return p



if __name__ == '__main__':


    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

            'resource': 'ornl.titan_orte',
            'walltime': 120,
            'cores': 32,
            'project': 'chm126',
            'queue': 'batch',
            'access_schema': 'local'
    }



    # Create Resource Manager object with the above resource description
    rman = ResourceManager(res_dict)

    # Create Application Manager
    appman = AppManager(hostname='openshift-node1.ccs.ornl.gov', port=30673, autoterminate = False)

    # Assign resource manager to the Application Manager
    appman.resource_manager = rman

    p = generate_pipeline()
    
    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set([p]))

    # Run the Application Manager
    appman.run()

    p = generate_pipeline()
    #print p.uid

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.assign_workflow(set([p]))

    # Run the Application Manager
    appman.run()

    appman.resource_terminate()