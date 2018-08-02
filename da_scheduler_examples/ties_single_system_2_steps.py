from radical.htbac import Ties, Runner
import os 

def main():

    ht = Runner()

    ties = Ties(number_of_replicas=5, number_of_windows=3, systems=['brd4-gsk3-1'], full=True)
                                                                  

    ht.add_protocol(ties)
    ht.cores = 24
    ht.rabbitmq_config(hostname='two.radical-project.org', port=33052)
    ht.run(walltime = 40)


if __name__ == '__main__':
        
    main()
