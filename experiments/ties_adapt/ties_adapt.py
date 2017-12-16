from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties2_3 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk2-3', full=False)

    ht.add_protocol(ties2_3)
    ht.cores = 64
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32800)
    ht.run()

    ties2_3_lds = Ties(number_of_replicas=5, additional=[0.15, 0.85], system='brd4-gsk2-3', full=False)

    ht.rerun(protocol=ties2_3_lds, terminate=True)


if __name__ == '__main__':
    main()
