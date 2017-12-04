from radical.htbac import htbac, Esmacs, Ties, Ties_EoP, Esmacs_7_stages


if __name__ == '__main__':

    ht = htbac.Runner()
    
    protocol_ties_instance_1   = Ties(replicas = 5, 
                                      lambda_initial = 0, 
                                      lambda_final = 1, 
                                      lambda_delta = 0.05, 
                                      rootdir = 'bace1_b01', 
                                      workflow = ['min', 'eq1', 'eq2', 'prod'])

    ht.add_protocol(protocol_ties_instance_1)
    

    #define number of cores as required by each task 
    #future: add another argument for cores to each protocol

    ht.cores = 32
    
    #define hostname and port for running rabbitmq
    
    ht.rabbitmq_config(hostname = 'two.radical-project.org', port = 32800)
    ht.run()
