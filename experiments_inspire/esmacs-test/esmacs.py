from radical.htbac import Esmacs, Runner


def main():

    ht = Runner()
    esm = Esmacs(number_of_replicas=1, systems = ['brd4-gsk2','brd4-gsk3'], full=False, cores=16)
    ht.add_protocol(esm)
    ht.rabbitmq_config(hostname='two.radical-project.org', port=33007)
    ht.run(walltime=90)

if __name__ == '__main__':
    main()
