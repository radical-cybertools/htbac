from radical.htbac import Esmacs, Runner


def main():
    ht = Runner()

    esmacs1 = Esmacs(number_of_replicas=25, system='brd4-gsk1')
    esmacs2 = Esmacs(number_of_replicas=25, system='brd4-gsk2')
    esmacs3 = Esmacs(number_of_replicas=25, system='brd4-gsk3')
    esmacs4 = Esmacs(number_of_replicas=25, system='brd4-gsk4')
    esmacs5 = Esmacs(number_of_replicas=25, system='brd4-gsk5')
    esmacs6 = Esmacs(number_of_replicas=25, system='brd4-gsk6')
    esmacs7 = Esmacs(number_of_replicas=25, system='brd4-gsk7')
    esmacs8 = Esmacs(number_of_replicas=25, system='brd4-gsk8')

    ht.add_protocol(esmacs1)
    ht.add_protocol(esmacs2)
    ht.add_protocol(esmacs3)
    ht.add_protocol(esmacs4)
    ht.add_protocol(esmacs5)
    ht.add_protocol(esmacs6)
    ht.add_protocol(esmacs7)
    ht.add_protocol(esmacs8)

    ht.cores = 64
    ht.rabbitmq_config(hostname='localhost', port=32821)
    ht.run()


if __name__ == '__main__':
    main()
