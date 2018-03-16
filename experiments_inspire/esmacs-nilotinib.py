from radical.htbac import Esmacs, Runner


def main():

    muts = ['e255k', 'e255v', 'e355a', 'e459k', 'f317c', 'f317i', 'f317l', 'f317v', 'f359c', 'f359i', 'f359v', 'g250e',
            'wt']
    #       'h396r', 'l248r', 'l248v', 'm244v', 'm351t', 't315a', 't315i', 'v299l', 'wt', 'y253f']

    ht = Runner()
    esm = Esmacs(number_of_replicas=25, systems=muts, full=True, cores=16, cutoff=10, water_model='tip4')
    ht.add_protocol(esm)

    ht.rabbitmq_config(hostname='openshift-node1.ccs.ornl.gov', port=30673)
    ht.run(walltime=720)


if __name__ == '__main__':
    main()
