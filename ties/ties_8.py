from radical.htbac import Esmacs, Runner, Ties


def main():

    ht = Runner()

    ties = Ties(number_of_replicas=5, number_of_windows=11, systems=(['brd4-gsk3-1',
                                                                     'brd4-gsk3-4',
                                                                     'brd4-gsk3-7',
                                                                     'brd4-gsk3-1-2',
                                                                     'brd4-gsk3-4-2',
                                                                     'brd4-gsk3-7-2',
                                                                     'brd4-gsk3-1-3',
                                                                     'brd4-gsk3-1-4']), cores=16, full=False)

    ht.add_protocol(ties)

    ht.rabbitmq_config(hostname='csc190specfem.marble.ccs.ornl.gov', port=30672) # add new port number 
    ht.run(walltime=120)


if __name__ == '__main__':
    main()
