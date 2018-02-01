from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esm = Esmacs(number_of_replicas=1, system='brd4-gsk2')

    ht.add_protocol(esm)
    
    ht.cores = 16
    ht.rabbitmq_config()
    ht.run()


if __name__ == '__main__':
    main()
