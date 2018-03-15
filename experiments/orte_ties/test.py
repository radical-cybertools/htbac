from radical.htbac import Ties, Runner


def main():

    ht = Runner()

    ties = Ties(number_of_replicas=5, number_of_windows=11, systems=['brd4-gsk3-1'])
                                                                  

    ht.add_protocol(ties)
    ht.cores = 16
    ht.rabbitmq_config(hostname='localhost', port=5672)
    

if __name__ == '__main__':
    main()


