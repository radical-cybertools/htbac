from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()
    esm = Esmacs(number_of_replicas=25, systems = (['brd4-gsk1',
                                                    'brd4-gsk2',
                                                    'brd4-gsk3',
                                                    'brd4-gsk4',
                                                    'brd4-gsk5',
                                                    'brd4-gsk6',
                                                    'brd4-gsk7',
                                                    'brd4-gsk8']), 
                                                    cores=32, full=False)
    ht.add_protocol(esm)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33130) # add new port number 
    ht.run(strong_scaled=1, autoterminate=True, queue='high', walltime=200)

if __name__ == '__main__':
    main()
