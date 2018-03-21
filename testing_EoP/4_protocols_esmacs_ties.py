from radical.htbac import Esmacs, Runner, Ties


def main():

    ht = Runner()

    esm1 = Esmacs(number_of_replicas = 25, system = 'brd4-gsk1', cores = 32, full=False) 
    esm2 = Esmacs(number_of_replicas=1, system='brd4-gsk2', cores=32, full=False)   
    ties1 = Ties(number_of_replicas = 5, number_of_windows = 13, system = 'brd4-gsk2-3', cores = 32, full = False)
    ties2 = Ties(number_of_replicas = 5, number_of_windows = 13, system = 'brd4-gsk3-1', cores = 32, full = False)

    ht.add_protocol(esm1)
    ht.add_protocol(esm2)
    
    ht.add_protocol(ties1)
    ht.add_protocol(ties2)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33048) # add new port number 
    ht.run(walltime=120)


if __name__ == '__main__':
    main()
