## How to run multiple instances of ESMACS and TIES protocols

0) Run setup.sh 
1) Define esmacs protocol: `esmacs(number_of_replicas, root_directory_of_system)`\
   Define ties protocol: `ties(number_of_replicas, lambda_initial, lambda_final, lambda_delta, root_directory_of_system, workflow_steps)`
2) Append protocols
3) Add the total number of cores required by all protocols
4) Specify resource configuration and rabbitMQ hostname/port
4) Run!

### Example below can be run with `running_multiple_workflows.py`

```python
from radical.htbac import htbac, Esmacs, Ties, Ties_EoP


if __name__ == '__main__':

    ht = htbac.Runner()

    protocol_esmacs_instance_1 = Esmacs(replicas = 25, 
                                        rootdir = 'sample_esmacs_data_system1.tgz')
    
    protocol_esmacs_instance_2 = Esmacs(replicas = 25, 
                                        rootdir = 'sample_esmacs_data_system2.tgz')
    
    protocol_ties_instance_1   = Ties(replicas = 65, 
                                      lambda_initial = 0, 
                                      lambda_final = 1, 
                                      lambda_delta = 0.05, 
                                      rootdir = 'bace1_b01', 
                                      workflow = ['min', 'eq1', 'eq2', 'prod'])

    #future: decouple steps in the workload, provide additional pertubations to the user for TIES

    ht.add_protocol(protocol_esmacs_instance_1)
    ht.add_protocol(protocol_esmacs_instance_2)
    ht.add_protocol(protocol_ties_instance_1)

    #define total number of cores as required by all protocol instances
    #future: add another argument for cores to each protocol

    ht.cores = 256 
    
    #define hostname and port for running rabbitmq
    
    ht.rabbitmq_config(hostname = 'two.radical-project.org', port = 32775)
    ht.run()
