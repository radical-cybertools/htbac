#running two esmacs and 1 ties instances:
'''

0) Run setup.sh 

1) Define esmacs protocol: esmacs(number_of_replicas, root_directory_of_system)
   Define ties protocol: ties(number_of_replicas, lambda_initial, lambda_final, lambda_delta, root_directory_of_system, workflow_steps)

2) Append protocols

3) Add the total number of cores required by all protocols

4) Specify resource configuration and rabbitMQ hostname/port

4) Run!

'''

from radical.htbac import htbac, Esmacs, Ties, Esmacs_MPI 


if __name__ == '__main__':

    ht = htbac.Runner()

    protocol_esmacs_instance_1 = Esmacs_MPI(replicas = 8, 
                                        rootdir = '2j6m-a698',
                                        workflow = ['eq0', 'eq1', 'eq2', 'prod'])

    protocol_esmacs_instance_2 = Esmacs_MPI(replicas = 8, 
                                        rootdir = '2j6m-a698_2',
                                        workflow = ['eq0', 'eq1', 'eq2', 'prod'])
    
    ht.add_protocol(protocol_esmacs_instance_1)
    ht.add_protocol(protocol_esmacs_instance_2)
    

    #define total number of cores as required by all protocol instances
    #future: add another argument for cores to each protocol

    ht.cores = 32
    
    #define hostname and port for running rabbitmq
    
    ht.rabbitmq_config(hostname = 'two.radical-project.org', port = 32804)
    ht.run()
