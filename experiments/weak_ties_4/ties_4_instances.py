from radical.htbac import Ties, Runner

def main():

    ht = Runner()

    ties = Ties(number_of_replicas=5, number_of_windows=11, systems='[brd4-gsk2-3',
                                                                    'brd4-gsk3-1',
                                                                    'brd4-gsk3-4',
                                                                    'brd4-gsk3-7'])
    #ties3_1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    #ties3_4 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-4')
    #ties3_7 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-7')

    ht.add_protocol(ties)
    #ht.add_protocol(ties3_1)
    #ht.add_protocol(ties3_4)
    #ht.add_protocol(ties3_7)
    ht.cores = 32
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32804)
    ht.run()


if __name__ == '__main__':
    main()
