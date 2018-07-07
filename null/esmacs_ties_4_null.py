from radical.htbac import Esmacs_null, Runner, Ties_null


def main():

    ht = Runner()

    esm1  = Esmacs_null(number_of_replicas = 25, 
        systems = ['brd4-gsk1','brd4-gsk2'], cores = 32, full=False) 
    ties1 = Ties_null(number_of_replicas = 5, number_of_windows = 13, 
        systems = ['brd4-gsk2-3','brd4-gsk3-1'], cores = 32, full = False)

    ht.add_protocol(esm1)    
    ht.add_protocol(ties1)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33048) # add new port number 
    ht.run(walltime=120)


if __name__ == '__main__':
    main()
