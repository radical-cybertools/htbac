from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties = Ties(number_of_replicas=5, number_of_windows=11, systems=['brd4-gsk3-1-2', 
                                                                     'brd4-gsk3-1-3',
                                                                     'brd4-gsk3-1-4',
                                                                     'brd4-gsk3-1-5',
                                                                     'brd4-gsk3-4-2',
                                                                     'brd4-gsk3-4-3',
                                                                     'brd4-gsk3-4-4',
                                                                     'brd4-gsk3-4-5'])
                                                                  

    ht.add_protocol(ties)
    ht.cores = 16
    ht.rabbitmq_config(hostname='openshift-node1.ccs.ornl.gov', port=30673)
    ht.run()

    ht.run()


if __name__ == '__main__':
    main()
