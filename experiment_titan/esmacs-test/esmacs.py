from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esm = Esmacs(number_of_replicas=1, system='brd4-gsk2', full=False)

    ht.add_protocol(esm)
    
    ht.cores = 16
    ht.rabbitmq_config(hostname='two.radical-project.org', port=33000)
    ht.run(walltime=90, strong_scaled=)


if __name__ == '__main__':
    main()
