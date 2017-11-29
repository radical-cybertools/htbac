#running two esmacs instances:

#define protocol_1 = esmacs(number_of_replicas, data_dir)
#define protocol_2 = esmacs(number_of_replicas, data_dir)
#define protocol_3 = ties(number_of_replicas, lambda_initial, lambda_final, lambda_delta, data_dir , workflow)

import radical.htbac as htbac 


if __name__ == '__main__':

    ht = htbac_runner()
    protocol_1 = esmacs(25, sample_esmacs_data.tgz)
    protocol_2 = esmacs(25, sample_esmacs_data.tgz)
    protocol_3 = ties(65, 0, 1, 0.05, bace1_b01, ['min', 'eq1', 'eq2', 'prod'])
    ht.add_protocol(protocol_1)
    ht.add_protocol(protocol_2)
    ht.add_protocol(protocol_3)
    ht.cores(256)
    ht.run
