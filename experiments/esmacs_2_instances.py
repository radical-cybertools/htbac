from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esmacs1 = Esmacs(number_of_replicas=25,
                     system='brd4-gsk1',
                     workflow=['eq0', 'eq1', 'eq2', 'sim1'])

    esmacs2 = Esmacs(number_of_replicas=25,
                     system='brd4-gsk2',
                     workflow=['eq0', 'eq1', 'eq2', 'sim1'])


    ht.add_protocol(esmacs1)
    ht.add_protocol(esmacs2)
    
    ht.cores = 64
    ht.rabbitmq_config(hostname='localhost', port=32808)
    ht.run()


if __name__ == '__main__':
    import os

    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'
    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://htbac-user:password@ds131826.mlab.com:31826/htbac-isc-experiments'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'
    os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'
    os.environ['RADICAL_PILOT_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILE'] = 'True'
    os.environ['RADICAL_ENMD_PROFILING'] = '1'

    main()