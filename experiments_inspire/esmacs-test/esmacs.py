from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esm1 = Esmacs(number_of_replicas=1, system='brd4-gsk2', full=False, cores=16)
    esm2 = Esmacs(number_of_replicas=1, system='brd4-gsk3', full=False, cores=16)

    ht.add_protocol(esm1)
    ht.add_protocol(esm2)

    ht.cores = 16
    ht.rabbitmq_config(hostname='two.radical-project.org', port=33000)
    ht.run(walltime=90)


if __name__ == '__main__':
    main()
