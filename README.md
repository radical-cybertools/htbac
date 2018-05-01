
# High Throughput Binding Affinity Calculator 

High performance execution framework for running molecular dynamics simulations locally or
on supercomputers. Create a workflow for your specific MD requirements and submit jobs on
thousands of nodes. 

## Features:

1. Support for combinatorial variable assignment: any parameter in the simulation can
take a list of values and a product of all variable combinations will be executed. For 
example you can have `system` attribute be a list of systems like `["protein-drug-1", 
"protein-drug-2"]` and your protocol will run for both systems. Or you want to experiment 
with certain parameters, like restrain strength: just tell the framework that your 
property will be a variable. 


## `Ensemble`s

It is common when running large scale MD simulations to execute the same template config
but having certain values take more than one value. Ensembles are an easy way to define
this in `htbac`.
