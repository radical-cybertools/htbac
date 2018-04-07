from radical.htbac import Esmacs, Runner, Ties


def main():

    ht = Runner()

    ties1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1-2', cores=32, full=False)
    ties2 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1-3', cores=32, full=False)
    ties3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1-4', cores=32, full=False)
    ties4 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1-5', cores=32, full=False)
    ties5 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4-2', cores=32, full=False)
    ties6 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4-3', cores=32, full=False)
    ties7 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4-4', cores=32, full=False)
    ties8 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4-5', cores=32, full=False)

    ht.add_protocol(ties1)
    ht.add_protocol(ties2)
    ht.add_protocol(ties3)
    ht.add_protocol(ties4)
    ht.add_protocol(ties5)
    ht.add_protocol(ties6)
    ht.add_protocol(ties7)
    ht.add_protocol(ties8)
    

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33126) # add new port number 
    ht.run(walltime=180)


if __name__ == '__main__':
    main()