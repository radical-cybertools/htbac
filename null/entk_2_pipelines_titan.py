
import os
from radical.entk import Pipeline, Stage, Task
from radical.entk import AppManager

# ------------------------------------------------------------------------------
# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'




if __name__ == '__main__':

    pipelines = set()
    p1 = Pipeline()
    
    
    for i in range(4):
        s = Stage()

        for x in range(10):
            t = Task()
            t.name = 'my-task'        # Assign a name to the task (optional, do not use ',' or '_')
            t.cpu_reqs = { 
                            'processes': 1,
                            'process_type': 'MPI',
                            'threads_per_process': 15,
                            'thread_type': None
                        }
        
            t.executable = ['/bin/hostname']   # Assign executable to the task   
            t.arguments = ['>','hostname_%s.txt'%x]  # Assign arguments for the task executable
            s.add_tasks(t)
            
        p1.add_stages(s)
        p2.add_stages(s)

    pipelines.add(p1)
    

    
    # appman = AppManager(hostname='two.radical-project.org', port=33048)
    amgr = AppManager(hostname='csc190specfem.marble.ccs.ornl.gov', port=30672)
    amgr.resource_desc = {'resource': 'ornl.titan_orte',
                            'walltime': 30,
                            'cpus': 160,
                            'project': 'chm126',
                            'queue': 'batch',
                            'access_schema': 'local'}
    amgr.workflow = pipelines

    # Assign resource request description to the Application Manager
    # resource_manager = ResourceManager(res_dict)
    # appman.resource_manager = resource_manager

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    # appman.assign_workflow(pipelines)

    # Run the Application Manager
    amgr.run()
