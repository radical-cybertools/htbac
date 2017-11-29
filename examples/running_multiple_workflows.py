#running two esmacs instances:

#define protocol_1(number_of_replicas, data_dir)

import radical.htbac as htbac 


if __name__ == '__main__':

    ht = htbac_runner()
    protocol_1 = esmacs(8, sample_esmacs_data.tgz)
    protocol_2 = esmacs(8, sample_esmacs_data.tgz)
    ht.add_protocol(protocol_1)
    ht.add_protocol(protocol_2)
    ht.cores(256)
    
    ht.run
