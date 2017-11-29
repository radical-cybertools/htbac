
# High Throughput Binding Affinity Calculator 

Framework supporting UCL ESMACS/TIES protocols 

## How to run: 

`pip install --process-dependency-links --upgrade .` 

`from htbac import htbac`

```
ht = htbac()
protocol_1 = esmacs(8, 2j6m-a698g)
protocol_2 = esmacs(8, 2j6m-a698g)
ht.add_protocol(protocol_1)
ht.add_protocol(protocol_2)
ht.cores(256)
ht.run
```
