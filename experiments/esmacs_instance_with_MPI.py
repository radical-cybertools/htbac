from radical.htbac import htbac, Esmacs, Ties, Ties_EoP, Esmacs_MPI 


if __name__ == '__main__':

    ht = htbac.Runner()

    protocol_esmacs_instance_1 = Esmacs_MPI(replicas = 8, 
                                        rootdir = '2j6m-a698g',
                                        workflow = ['eq0', 'eq1', 'eq2', 'prod'])
    
    ht.add_protocol(protocol_esmacs_instance_1)
    

    #define total number of cores as required by all protocol instances
    #future: add another argument for cores to each protocol

    ht.cores = 32
    
    #define hostname and port for running rabbitmq
    
    ht.rabbitmq_config(hostname = 'two.radical-project.org', port = 32775)
    ht.run()
