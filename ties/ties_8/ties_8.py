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
                                                                     'brd4-gsk3-1-4']), cores=32, full=False)
    ht.add_protocol(ties)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33126) # add new port number 
    ht.run(queue='high', walltime=180)


if __name__ == '__main__':
    main()