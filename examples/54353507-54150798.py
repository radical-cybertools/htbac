from htbac import Runner, Protocol, Simulation, System, AbFile, DataAggregate


# define system
pdb = AbFile('systems/54353507-54150798/54353507-54150798-complex.pdb', tag='pdb')
top = AbFile('systems/54353507-54150798/54353507-54150798-complex.top', tag='topology')
tag = AbFile('systems/54353507-54150798/54353507-54150798-tags.pdb', tag='alchemicaltags')
cor = AbFile('systems/54353507-54150798/54353507-54150798-complex.crd', tag='coordinate')
cons = AbFile('systems/54353507-54150798/54353507-54150798-cons.pdb', tag='constraint')
fep = AbFile('systems/54353507-54150798/54353507-54150798-fep.tcl', tag='source')
system = System(name='54353507-54150798', files=[pdb, top, tag, cor, cons, fep])


# Create simulation steps for relative free energy protocol

# define protocol:
p = Protocol()

# define step 0: 
s0 = Simulation(name='minimizer')
s0.engine = 'namd'
s0.processes = 32
s0.threads_per_process = 1
s0.add_ensemble('replica', range(5))
s0.add_ensemble('lambdawindow', [1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 
            0.30, 0.20, 0.10, 0.05, 0.00])
s0.add_input_file("default_configs/rfe/54353507-54150798/eq0.conf", is_executable_argument=True)
s0.system = system


s0.cutoff = 12.0
s0.switchdist = 10.0
s0.pairlistdist = 13.5
s0.numsteps = 1000


# append step 0 to protocol:
p.append(s0)

# define step 1: 
s1 = Simulation(name='equilibrate1')
s1.engine = 'namd'
s1.processes = 32
s1.threads_per_process = 1
s1.add_ensemble('replica', range(5))
s1.add_ensemble('lambdawindow', [1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 
            0.30, 0.20, 0.10, 0.05, 0.00])
s1.add_input_file("default_configs/rfe/54353507-54150798/eq1.conf", is_executable_argument=True)
s1.system = system

# <placeholders>
s1.cutoff = 12.0
s1.switchdist = 10.0
s1.pairlistdist = 13.5
s1.numsteps = 30000 


# append step 1 to protocol:
p.append(s1)


# define step 3: 
s2 = Simulation(name='equilibrate2')
s2.engine = 'namd'
s2.processes = 32
s2.threads_per_process = 1
s2.add_ensemble('replica', range(5))
s2.add_ensemble('lambdawindow', [1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 
            0.30, 0.20, 0.10, 0.05, 0.00])
s2.add_input_file("default_configs/rfe/54353507-54150798/eq2.conf", is_executable_argument=True)
s2.system = system

# <placeholders>
s2.cutoff = 12.0
s2.switchdist = 10.0
s2.pairlistdist = 13.5
s2.numsteps = 970000 


# append step 4 to protocol:
p.append(s2)


# define step 4: 
s3 = Simulation(name='production')
s3.engine = 'namd'
s3.processes = 32
s3.threads_per_process = 1
s3.add_ensemble('replica', range(5))
s3.add_ensemble('lambdawindow', [1.00, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 
            0.30, 0.20, 0.10, 0.05, 0.00])
s3.add_input_file("default_configs/rfe/54353507-54150798/sim.conf", is_executable_argument=True)
s3.system = system

# <placeholders>
s3.cutoff = 12.0
s3.switchdist = 10.0
s3.pairlistdist = 13.5
s3.numsteps = 2000000 


# append step 4 to protocol:
p.append(s3)

p.append(DataAggregate(extension=".alch"))

ht = Runner('bw_aprun', comm_server=('two.radical-project.org', 33048))

ht.add_protocol(p)
ht.run(walltime=480)
