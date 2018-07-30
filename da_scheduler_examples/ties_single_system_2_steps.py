from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties = Ties(number_of_replicas=5, number_of_windows=11, systems=['brd4-gsk3-1'], full=True)
                                                                  

    ht.add_protocol(ties)
    ht.cores = 32
    ht.rabbitmq_config(hostname='two.radical-project.org', port=33048)
    ht.run(walltime = 30)


if __name__ == '__main__':
    main()
