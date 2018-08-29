.. _installation:

************
Installation
************

Installing HTBAC
===========================

To install HTBAC, we need to create a virtual or conda environment . Open a terminal and run:

.. code-block:: bash

        virtualenv $HOME/venv
        source $HOME/venv/bin/activate

        conda create -n venv python=2.7
        source activate venv


HTBAC uses the `Ensemble Toolkit <https://radicalentk.readthedocs.io/en/latest/>`_ to execute ensemble-based workflows. 
Install the Ensemble Toolkit before installing HTBAC by accessing the `installation guide <https://radicalentk.readthedocs.io/en/latest/install.html>`_. 

Once the Ensemble Toolkit is properly installed, install HTBAC by running the following commands:

.. code-block:: bash

        git clone https://github.com/radical-cybertools/htbac.git
        cd htbac
        pip install .



Preparing the Environment
=========================

HTBAC uses `RADICAL Pilot <http://radicalpilot.readthedocs.org>`_ as 
the runtime system. RADICAL Pilot can access HPC clusters remotely via SSH and 
GSISSH, but it requires (a) a MongoDB server and (b) a properly set-up 
passwordless SSH/GSISSH environment.


MongoDB Server
--------------

.. figure:: figures/hosts_and_ports.png
     :width: 360pt
     :align: center
     :alt: MongoDB and SSH ports.

The MongoDB server is used to store and retrieve operational data during the
execution of an application using RADICAL-Pilot. The MongoDB server must
be reachable on **port 27017** from **both**, the host that runs the
HTBAC application and the host that executes the MD tasks, i.e.,
the HPC cluster (see blue arrows in the figure above). In our experience,
a small VM instance (e.g., Amazon AWS) works exceptionally well for this.

.. warning:: If you want to run your application on your laptop or private
            workstation, but run your MD tasks on a remote HPC cluster,
            installing MongoDB on your laptop or workstation won't work.
            Your laptop or workstations usually does not have a public IP
            address and is hidden behind a masked and firewalled home or office
            network. This means that the components running on the HPC cluster
            will not be able to access the MongoDB server.

A MongoDB server can support more than one user. In an environment where
multiple users use Ensemble Toolkit, a single MongoDB server
for all users / hosts is usually sufficient.

**Install your own MongoDB**

Once you have identified a host that can serve as the new home for MongoDB,
installation is straight forward. You can either install the MongoDB
server package that is provided by most Linux distributions, or
follow the installation instructions on the MongoDB website:

http://docs.mongodb.org/manual/installation/

**MongoDB-as-a-Service**

There are multiple commercial providers of hosted MongoDB services, some of them
offering free usage tiers. We have had some good experience with the following:

* https://mongolab.com/


.. _ssh_gsissh_setup:

Setup passwordless SSH Access to machines
-----------------------------------------

In order to create a passwordless access to another machine, you need to create a RSA key on your local machine
and paste the public key into the `authorizes_users` list on the remote machine.

`This <http://linuxproblem.org/art_9.html>`_ is a recommended tutorial to create password ssh access.

An easy way to setup SSH access to multiple remote machines is to create a file ``~/.ssh/config``.
Suppose the url used to access a specific machine is ``foo@machine.example.com``. You can create an entry in this 
config file as follows:

.. code-block:: bash

        # contents of $HOME/.ssh/config
        Host machine1
                HostName machine.example.com
                User foo

Now you can login to the machine by ``ssh machine1``.


Source: http://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/


Setup GSISSH Access to a machine
---------------------------------

Setting up GSISSH access to a machine is a bit more complicated. We have documented the steps to setup GSISSH on
`Ubuntu <https://github.com/vivek-bala/docs/blob/master/misc/gsissh_setup_stampede_ubuntu_xenial.sh>`_ (tested for 
trusty and xenial) and `Mac <https://github.com/vivek-bala/docs/blob/master/misc/gsissh_setup_mac>`_. Simply execute 
all the commands, see comments for details.

The above links document the overall procedure and get certificates to access XSEDE machines. Depending on the machine
you want to access, you will have to get the certificates from the corresponding locations. In most cases, this
information is available in their user guide. 


Troubleshooting
=======================

**Missing virtualenv**

This should return the version of the RADICAL-Pilot installation, e.g., `0.X.Y`.

If virtualenv **is not** installed on your system, you can try the following.

.. code-block:: bash

        wget --no-check-certificate https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
        tar xzf virtualenv-1.9.tar.gz

        python virtualenv-1.9/virtualenv.py $HOME/myenv
        source $HOME/myenv/bin/activate

**TypeError: 'NoneType' object is not callable**

Note that some Python installations have a broken multiprocessing module -- if you
experience the following error during installation::

    Traceback (most recent call last):
        File "/usr/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
            func(*targs, **kargs)
        File "/usr/lib/python2.7/multiprocessing/util.py", line 284, in _exit_function
            info('process shutting down')
    TypeError: 'NoneType' object is not callable

    you may need to move to Python 2.7 (see http://bugs.python.org/issue15881).