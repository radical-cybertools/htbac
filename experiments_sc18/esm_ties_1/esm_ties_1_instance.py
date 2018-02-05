from radical.htbac import Ties, Esmacs, Runner


def main():

    ht = Runner()

    ties2_3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3')
    esmacs1 = Esmacs(number_of_replicas=25, system='brd4-gsk1')

    ht.add_protocol(ties2_3)
    ht.add_protocol(esmacs1)
    ht.cores = 64
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32775)
    ht.run()


if __name__ == '__main__':
    main()
