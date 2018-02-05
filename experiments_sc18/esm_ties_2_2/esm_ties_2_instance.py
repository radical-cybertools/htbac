from radical.htbac import Ties, Esmacs, Runner


def main():

    ht = Runner()

    ties3_4 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4')
    esmacs2 = Esmacs(number_of_replicas=25, system='brd4-gsk2')
    ties3_1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    esmacs3 = Esmacs(number_of_replicas=25, system='brd4-gsk3')

    ht.add_protocol(ties3_4)
    ht.add_protocol(esmacs2)
    ht.add_protocol(ties3_1)
    ht.add_protocol(esmacs3)
    ht.cores = 64
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32800)
    ht.run()


if __name__ == '__main__':
    main()
