Modular, Recognizing System for Quantification of Uncertainty with Ensembles (MoReSQUE)
=======================================================================================

The provided packages are supplementary material for the PhD thesis
"A Non-Intrusive Uncertainty Quantification System for Modular Smart Grid Co-Simulation"
by Cornelius Steinbrink.

Repository Structure
--------------------

The code of the uncertainty quantification system itself is given in the folder
"moresque". Furthermore, two example studies are provided to illustrate the
utilization of the moresque software.
The folder "example_pv" contains a simple example with only two interconnected
simulators (solar irradiation and pv panel) and purely interval-based uncertainty representation.
The folder "example_scenario", on the other hand, provides a more complex example
with more (and partly composite) simulators and different forms of uncertainty
representation.

The code of all simulators used for the examples is given in the folder
"simulators_for_example".
Code for further testing is provided in the folder "testing_utility_components".
It contains the module "sim_testbench" that includes a Monte Carlo Simulation module as an alternative to MoReSQUE 
for UQ in mosaik. The other modules provide
basic input and output capabilities for MoReSQUE as well as MCS in order to
enable UQ studies with single simulators.

Installation
------------

The MoReSQUE software package has been developed and tested solely under Linux.

Installation of MoReSQUE may be conducted via::

    $ pip install .

in the "moresque" folder (the folder with the setup.py script).
This automatically installs all dependencies:
mosaik-api,
numpy,
scipy,
pyDOE,
arrow,
statsmodels

In order to run the example, mosaik has to be installed via:
$ pip install mosaik
Furthermore, the packages in the folder "simulators_for_example" have to be
installed. The all include setup.py scripts so that the are installed the same
way as MoReSQUE. In order to install the database module "mosaik-hdf5" it
typically is necessary to first run::

    $ pip install Cython
    $ pip install h5py

All other dependencies should be correctly installed with the particular
installation scripts.
