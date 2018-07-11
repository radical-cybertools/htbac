
import os
from radical.entk import Pipeline, Stage, Task
from radical.entk import AppManager, ResourceManager

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

    pipelines = set()
    p1 = Pipeline()
    p2 = Pipeline()
    
    for i in range(4):
        s = Stage()

        for x in range(10):
            t = Task()
            t.name = 'my-task'        # Assign a name to the task (optional, do not use ',' or '_')
            t.cpu_reqs = { 
                            'processes': 1,
                            'process_type': None,
                            'threads_per_process': 15,
                            'thread_type': None
                        }
        
            t.executable = ['/bin/hostname']   # Assign executable to the task   
            t.arguments = ['>','hostname_%s.txt'%x]  # Assign arguments for the task executable
            s.add_tasks(t)
            
        p1.add_stages(s)
        p2.add_stages(s)

    pipelines.add(p1)
    pipelines.add(p2) 

    
    # appman = AppManager(hostname='two.radical-project.org', port=33048)
    amgr = AppManager(hostname='two.radical-project.org', port=33048)
    amgr.resource_desc = {'resource': 'ncsa.bw_aprun',
                            'walltime': 30,
                            'cpus': 640
                            'project': 'bamm',
                            'queue': 'high',
                            'access_schema': 'gsissh'}
    amgr.workflow = pipelines

    # Assign resource request description to the Application Manager
    # resource_manager = ResourceManager(res_dict)
    # appman.resource_manager = resource_manager

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    # appman.assign_workflow(pipelines)

    # Run the Application Manager
    appman.run()
