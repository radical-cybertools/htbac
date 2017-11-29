#running two esmacs instances:

import htbac as htbac 

if __name__ == '__main__':

    ht = htbac_runner()
    protocol_1 = esmacs(8, sample_esmacs_data.tgz)
    protocol_2 = esmacs(8, 2j6m-a698g)
    ht.add_protocol(protocol_1)
    ht.add_protocol(protocol_2)
    ht.cores(256)
    
    ht.run
