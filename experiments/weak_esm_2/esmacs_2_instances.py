from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()

    esmacs2 = Esmacs(number_of_replicas=25, system='brd4-gsk2')
    esmacs3 = Esmacs(number_of_replicas=25, system='brd4-gsk3')

    ht.add_protocol(esmacs2)
    ht.add_protocol(esmacs3)
    
    ht.cores = 64
    ht.rabbitmq_config(hostname='localhost', port=32808)
    ht.run()


if __name__ == '__main__':
    main()
