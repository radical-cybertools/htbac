from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esm1 = Esmacs(number_of_replicas=1, system='brd4-gsk1', cores=32, full=False)
    esm2 = Esmacs(number_of_replicas=1, system='brd4-gsk2', cores=32, full=False)

    ht.add_protocol(esm1)
    ht.add_protocol(esm2)


    ht.rabbitmq_config(hostname='two.radical-project.org', port=33072) # add new port number 
    ht.run(walltime=120)


if __name__ == '__main__':
    main()
