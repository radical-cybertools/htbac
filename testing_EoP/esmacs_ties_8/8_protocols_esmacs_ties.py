from radical.htbac import Esmacs, Runner, Ties


def main():

    ht = Runner()

    esm1 = Esmacs(number_of_replicas=25, system='brd4-gsk1', cores=32, full=False)
    esm2 = Esmacs(number_of_replicas=25, system='brd4-gsk2', cores=32, full=False)
    esm3 = Esmacs(number_of_replicas=25, system='brd4-gsk3', cores=32, full=False)
    esm4 = Esmacs(number_of_replicas=25, system='brd4-gsk4', cores=32, full=False)

    ties2_3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3')
    ties3_1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    ties3_4 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4')
    ties3_7 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-7')

    ht.add_protocol(esm1)
    ht.add_protocol(esm2)
    ht.add_protocol(esm3)
    ht.add_protocol(esm4)
    
    ht.add_protocol(ties2_3)
    ht.add_protocol(ties3_1)
    ht.add_protocol(ties3_4)
    ht.add_protocol(ties3_7)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33048) # add new port number 
    ht.run(walltime=720)


if __name__ == '__main__':
    main()
