from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties3_7 = Ties(number_of_replicas=5, number_of_windows=11, systems=['brd4-gsk3-7','brd4-gsk3-1'], cores=32)
    #ties3_1 = Ties(number_of_replicas=1, number_of_windows=1, system='brd4-gsk3-1', cores=32)

    ht.add_protocol(ties3_7)
    #ht.add_protocol(ties3_1)
    ht.cores = 32
    #ht.rabbitmq_config(hostname='two.radical-project.org', port=32865)
    ht.run()


if __name__ == '__main__':
    main()
