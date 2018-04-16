from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()
    esm = Esmacs(number_of_replicas=25, systems = (['brd4-gsk1',
                                                    'brd4-gsk2']), 
                                                    cores=32, full=False)
    ht.add_protocol(esm)

    ht.rabbitmq_config(hostname='two.radical-project.org', port=33072) # add new port number 
    ht.run(strong_scaled=1, autoterminate=True, queue='debug', walltime=30):


if __name__ == '__main__':
    main()
