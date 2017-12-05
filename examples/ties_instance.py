from radical.htbac import Ties, Runner2


def main():

    ht = Runner2()

    ties = Ties(number_of_replicas=5,
                workflow=['min', 'eq1', 'eq2', 'prod'],
                system='complex',
                box=[5, 5, 5],
                lambda_delta=0.1)

    ht.add_protocol(ties)
    ht.cores = 32
    ht.rabbitmq_config()
    ht.run()


if __name__ == '__main__':
    import os

    os.environ['RADICAL_ENTK_VERBOSE'] = 'DEBUG'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://radical:fg*2GT3^eB@crick.chem.ucl.ac.uk:27017/admin'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
    os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'
    os.environ['RADICAL_PILOT_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILING'] = '1'

    main()
