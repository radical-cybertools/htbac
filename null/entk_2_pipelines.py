
import os
from radical.entk import Pipeline, Stage, Task, AppManager
# ------------------------------------------------------------------------------
# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('two.radical-project.org', '33048')
port = os.environ.get('two.radical-project.org', 33048)

if __name__ == '__main__':

    pipelines = []

    # Create a Pipeline object
    p1 = Pipeline()

    # Create Stage objects

    for i in range(4): 

        s = Stage()


        for cnt in range(10):

            # Create a Task object
            t = Task()
            t.name = 'my-task'        # Assign a name to the task (optional, do not use ',' or '_')
            t.executable = ['/bin/sleep']   # Assign executable to the task   
            t.arguments = ['1000']  # Assign arguments for the task executable

            # Add the Task to the Stage
            s.add_tasks(t)

    # Add Stage to the Pipeline
    p1.add_stages(s)
    pipelines.append(p1)

    # Create a Pipeline object
    p2 = Pipeline()

    # Create Stage objects

    for i in range(4): 

        s = Stage()


        for cnt in range(10):

            # Create a Task object
            t = Task()
            t.cores = 32
            t.mpi = True
            t.name = 'my-task'        # Assign a name to the task (optional, do not use ',' or '_')
            t.executable = ['/bin/sleep']   # Assign executable to the task   
            t.arguments = ['1000']  # Assign arguments for the task executable

            # Add the Task to the Stage
            s.add_tasks(t)

    # Add Stage to the Pipeline
    p2.add_stages(s)
    
    pipelines.append(p2)
    # Create Application Manager
    appman = AppManager(hostname='two.radical-project.org', port=33048)

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, and cpus
    # resource is 'local.localhost' to execute locally
    res_dict = {'resource': 'ncsa.bw_aprun',
                'walltime': 30,
                'cores': 640,
                'project': 'bamm',
                'queue': 'high',
                'access_schema': 'gsissh'}

    # Assign resource request description to the Application Manager
    appman.resource_desc = res_dict

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    appman.workflow = set(pipelines)

    # Run the Application Manager
    appman.run()
