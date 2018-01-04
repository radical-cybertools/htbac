from radical.htbac import Ties, Esmacs, Runner


def main():

    ht = Runner()

    ties3_4 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4')
    esmacs4 = Esmacs(number_of_replicas=25, system='brd4-gsk4')
    ties3_1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    esmacs5 = Esmacs(number_of_replicas=25, system='brd4-gsk5')
    ties3_7 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-7')
    esmacs6 = Esmacs(number_of_replicas=25, system='brd4-gsk6')
    ties2_3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3')
    esmacs7 = Esmacs(number_of_replicas=25, system='brd4-gsk7')

    ht.add_protocol(ties3_4)
    ht.add_protocol(esmacs4)
    ht.add_protocol(ties3_1)
    ht.add_protocol(esmacs5)
    ht.add_protocol(ties3_7)
    ht.add_protocol(esmacs6)
    ht.add_protocol(ties2_3)
    ht.add_protocol(esmacs7)

    ht.cores = 64
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32804)
    ht.run()


if __name__ == '__main__':
    main()
