from radical.htbac import Ties_nonLFS, Runner


def main():

    ht = Runner()

    ties = Ties_nonLFS(number_of_replicas=5, number_of_windows=3, systems=['brd4-gsk3-1'], full=True)
                                                                  

    ht.add_protocol(ties)
    ht.cores = 32
    ht.rabbitmq_config(hostname='two.radical-project.org', port=33130)
    ht.run(walltime = 40)


if __name__ == '__main__':
    
    os.environ['SAGA_PTY_SSH_TIMEOUT'] = '2000'
    os.environ['RADICAL_PILOT_PROFILE'] = True
    os.environ['RADICAL_ENTK_PROFILE'] = True
    os.environ['RADICAL_VERBOSE'] = True
    os.environ['PATH'] = '/usr/sbin:$PATH'

    main()
