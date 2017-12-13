from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties2_3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3')
    ties3_1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    ties3_4 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4')
    ties3_7 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-7')
    ties2_3_2 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3')
    ties3_1_2 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    ties3_4_2 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4')
    ties3_7_2 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-7')

    ht.add_protocol(ties2_3)
    ht.add_protocol(ties3_1)
    ht.add_protocol(ties3_4)
    ht.add_protocol(ties3_7)
    ht.add_protocol(ties2_3_2)
    ht.add_protocol(ties3_1_2)
    ht.add_protocol(ties3_4_2)
    ht.add_protocol(ties3_7_2)

    ht.cores = 64
    ht.rabbitmq_config()
    ht.run()


if __name__ == '__main__':
    main()
