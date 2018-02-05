from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties2_3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3')
    ties3_1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')

    ht.add_protocol(ties2_3)
    ht.add_protocol(ties3_1)
    ht.cores = 64
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32775)
    ht.run()


if __name__ == '__main__':
    main()
