from scipy import stats
import numpy as np

from radical.htbac import TiesEquilibration, TiesProduction, TiesAnalysis, Runner


def main():

    ht = Runner()

    ties2_3 = TiesEquilibration(number_of_replicas=1, number_of_windows=1, system='brd4-gsk2-3', full=False)

    ht.add_protocol(ties2_3)
    ht.cores = 64
    ht.rabbitmq_config(hostname='two.radical-project.org', port=32800)
    ht.run(autoterminate=False, queue='debug', walltime=30)

    print 'Equilibration finished'

    ties2_3_lds = TiesProduction(number_of_replicas=1, number_of_windows=1, system='brd4-gsk2-3', full=False)

    ht.rerun(protocol=ties2_3_lds, terminate=False, previous_pipeline=ties2_3)

    print 'Production finished'

    ties2_3_ana = TiesAnalysis(number_of_replicas=1, lambda_windows=ties2_3_lds.lambdas)

    ht.rerun(protocol=ties2_3_ana, terminate=True, previous_pipeline=ties2_3_lds)

    print 'Analysis finished'


if __name__ == '__main__':
    main()
