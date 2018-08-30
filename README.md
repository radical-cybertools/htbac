
# High Throughput Binding Affinity Calculator 

* High performance bio-simulation framework for running molecular dynamics simulations locally or
on supercomputers. Create a workflow for your specific MD requirements and submit jobs to a
cluster of [choice](https://radicalpilot.readthedocs.io/en/latest/resources.html#chapter-resources) 

* For documentation please visit [readthedocs](https://htbac.readthedocs.io/en/latest/)

## Features:

* HTBAC supports combinatorial variable assignment: any parameter in the simulation can
take a list of values and a product of all variable combinations will be executed. For 
example you can have `system` attribute be a list of systems like `["protein-drug-1", 
"protein-drug-2"]` and your protocol will run for both systems. Or you want to experiment 
with certain parameters, like restrain strength: just tell the framework that your 
property will be a variable. 

## Examples:

* [Jupyter Notebook](https://github.com/radical-cybertools/htbac/blob/master/examples/htbac.ipynb)
* Example scripts can be found [here](https://github.com/kristofarkas/abigail-experiments).
