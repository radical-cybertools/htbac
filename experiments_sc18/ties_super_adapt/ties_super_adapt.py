from radical.htbac import TiesEquilibration, TiesProduction, TiesAnalysis, Runner, AdaptiveQuadrature


def main():

    ht = Runner()

    ties2_3 = TiesEquilibration(number_of_replicas=2, number_of_windows=2, system='brd4-gsk2-3', full=False, cores=128)

    ht.add_protocol(ties2_3)
    ht.cores = 128
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32861)
    ht.run(autoterminate=False, queue='debug', walltime=30)

    print 'Equilibration finished'

    ties2_3_p1 = TiesProduction(number_of_replicas=2, number_of_windows=2, system='brd4-gsk2-3', full=False, cores=128)

    ht.rerun(protocol=ties2_3_p1, terminate=False, previous_pipeline=ties2_3)

    print 'Production 1 finished'

    aq = AdaptiveQuadrature('dg_{}.out'.format(ties2_3_p1.id()))

    ties2_3_p2 = TiesProduction(number_of_replicas=2, additional=aq.requested_windows(), system='brd4-gsk2-3', full=False, cores=64)

    ht.rerun(protocol=ties2_3_p2, terminate=False, previous_pipeline=ties2_3_p1)

    print 'Production 2 finished'

    aq = AdaptiveQuadrature('dg_{}.out'.format(ties2_3_p2.id()))

    ties2_3_p3 = TiesProduction(number_of_replicas=2, additional=aq.requested_windows(), system='brd4-gsk2-3', full=False, cores=32)

    ht.rerun(protocol=ties2_3_p3, terminate=False, previous_pipeline=ties2_3_p2)

    print 'Production 3 finished'

    ties2_3_p4 = TiesProduction(number_of_replicas=2, additional=ties2_3_p3.lambdas, system='brd4-gsk2-3', full=False, cores=32)

    ht.rerun(protocol=ties2_3_p4, terminate=True, previous_pipeline=ties2_3_p3)

    print 'Production 4 finished'


if __name__ == '__main__':
    main()
