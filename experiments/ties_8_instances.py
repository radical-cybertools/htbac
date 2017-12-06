from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties1 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk3-1')

    ties2 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk3-4')

    ties3 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk3-7')

    ties4 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk2-3')

    ties5 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk3-1')

    ties6 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk3-4')

    ties7 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk3-7')

    ties8 = Ties(number_of_replicas=5, number_of_windows=11,
                 workflow=['min', 'eq1', 'eq2', 'prod'],
                 system='brd4-gsk2-3')

    ht.add_protocol(ties1)
    ht.add_protocol(ties2)
    ht.add_protocol(ties3)
    ht.add_protocol(ties4)
    ht.add_protocol(ties5)
    ht.add_protocol(ties6)
    ht.add_protocol(ties7)
    ht.add_protocol(ties8)

    ht.cores = 32
    ht.rabbitmq_config()
    ht.run()


if __name__ == '__main__':
    import os

    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://radical:fg*2GT3^eB@crick.chem.ucl.ac.uk:27017/admin'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
    os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'
    os.environ['RADICAL_PILOT_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILING'] = '1'

    main()
