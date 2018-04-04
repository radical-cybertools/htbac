from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esm1 = Esmacs(number_of_replicas=25, system='brd4-gsk1', cores=32, full=False)
    esm2 = Esmacs(number_of_replicas=25, system='brd4-gsk2', cores=32, full=False)
    esm3 = Esmacs(number_of_replicas=25, system='brd4-gsk3', cores=32, full=False)
    esm4 = Esmacs(number_of_replicas=25, system='brd4-gsk4', cores=32, full=False)

    esm5 = Esmacs(number_of_replicas=25, system='brd4-gsk5', cores=32, full=False)
    esm6 = Esmacs(number_of_replicas=25, system='brd4-gsk6', cores=32, full=False)
    esm7 = Esmacs(number_of_replicas=25, system='brd4-gsk7', cores=32, full=False)
    esm8 = Esmacs(number_of_replicas=25, system='brd4-gsk8', cores=32, full=False)
    
    ht.add_protocol(esm1)
    ht.add_protocol(esm2)
    ht.add_protocol(esm3)
    ht.add_protocol(esm4)
    ht.add_protocol(esm5)
    ht.add_protocol(esm6)
    ht.add_protocol(esm7)
    ht.add_protocol(esm8)


    ht.rabbitmq_config(hostname='two.radical-project.org', port=33064) # add new port number 
    ht.run(walltime=120)


if __name__ == '__main__':
    main()
