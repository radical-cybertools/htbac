from radical.htbac import Ties, Esmacs, Runner


def main():

    ht = Runner()

    ties3_1 = Ties(number_of_replicas=2, number_of_windows=3,
                   workflow=['min', 'eq1', 'eq2', 'prod'],
                   system='brd4-gsk3-1')

    esmacs1 = Esmacs(number_of_replicas=5,
                     system='brd4-gsk1',
                     workflow=['eq0', 'eq1', 'eq2', 'sim1'])

    ht.add_protocol(ties3_1)
    ht.add_protocol(esmacs1)
    ht.cores = 32
    ht.rabbitmq_config()
    ht.run(walltime=1440, strong_scaled=0.5)


if __name__ == '__main__':
    main()
