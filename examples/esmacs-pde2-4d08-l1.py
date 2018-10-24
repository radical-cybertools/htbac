from htbac import Runner, Protocol, Simulation, System, AbFile, DataAggregate


# define system
pdb = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-complex.pdb', tag='pdb')
top = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-complex.top', tag='topology')
cons = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-f4.pdb', tag='constraint')
cor = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-complex.crd', tag='coordinate')
fep = AbFile('systems/esmacs-pde2-4d08-l1/esmacs-pde2-4d08-l1-fep.tcl', tag='source')
system = System(name='esmacs-pde2-4d08-l1', files=[pdb, top, cons, cor, fep])


# Create simulation steps for relative free energy protocol

# define protocol:
p = Protocol()

# define step 0: 
s0 = Simulation(name='stage-0')
s0.engine = 'namd'
s0.processes = 32
s0.threads_per_process = 1
s0.add_ensemble('replica', range(25))
s0.add_input_file("default_configs/esmacs/esmacs-pde2-4d08-l1/esmacs-stage-0.conf", is_executable_argument=True)
s0.system = system


s0.cutoff = 12.0
s0.switchdist = 10.0
s0.pairlistdist = 13.5
s0.numsteps = 1000
s0.numsmallsteps = 100
s0.constraint_column = "B"


# append step 0 to protocol:
p.append(s0)

# define step 1: 
s1 = Simulation(name='stage-1')
s1.engine = 'namd'
s1.processes = 32
s1.threads_per_process = 1
s1.add_ensemble('replica', range(25))
s1.add_input_file("default_configs/esmacs/esmacs-pde2-4d08-l1/esmacs-stage-1.conf", is_executable_argument=True)
s1.system = system

# <placeholders>
s1.cutoff = 12.0
s1.switchdist = 10.0
s1.pairlistdist = 13.5
s1.numsteps = 30000 


# append step 1 to protocol:
p.append(s1)


# define step 3: 
s2 = Simulation(name='stage-2')
s2.engine = 'namd'
s2.processes = 32
s2.threads_per_process = 1
s2.add_ensemble('replica', range(25))
s2.add_input_file("default_configs/esmacs/esmacs-pde2-4d08-l1/esmacs-stage-2.conf", is_executable_argument=True)
s2.system = system

# <placeholders>
s2.cutoff = 12.0
s2.switchdist = 10.0
s2.pairlistdist = 13.5
s2.numsteps = 470000
s2.numsmallsteps = 50000 


# append step 4 to protocol:
p.append(s2)


# define step 4: 
s3 = Simulation(name='stage-3')
s3.engine = 'namd'
s3.processes = 32
s3.threads_per_process = 1
s3.add_ensemble('replica', range(25))
s3.add_input_file("default_configs/esmacs/esmacs-pde2-4d08-l1/esmacs-stage-3.conf", is_executable_argument=True)
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
ht.run(walltime=2880)
