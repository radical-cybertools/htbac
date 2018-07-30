from radical.htbac import Esmacs, Runner, Ties


def main():

    ht = Runner()

    esm = Esmacs(number_of_replicas = 25, cores=32, full=False, systems = ['brd4-gsk1',
                                                                            'brd4-gsk2',
                                                                            'brd4-gsk3',
                                                                            'brd4-gsk4'])

    

    ties = Ties(number_of_replicas=5, number_of_windows=11, full=False, cores = 32, systems = ['brd4-gsk2-3',
                                                                                                'brd4-gsk3-1',
                                                                                                'brd4-gsk3-4',
                                                                                                'brd4-gsk3-7']

    

    ht.add_protocol(esm)
    ht.add_protocol(ties)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33126) # add new port number 
    ht.run(walltime=720, strong_scaled = 1)


if __name__ == '__main__':
    main()
