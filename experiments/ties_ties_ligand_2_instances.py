from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties1 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1')
    ties2 = Ties(number_of_replicas=5, number_of_windows=11, system='brd4-gsk3-1', ligand=True)

    ht.add_protocol(ties1)
    ht.add_protocol(ties2)
    ht.cores = 64
    ht.rabbitmq_config()
    ht.run(walltime=1440, strong_scaled=0.5)


if __name__ == '__main__':
    main()
