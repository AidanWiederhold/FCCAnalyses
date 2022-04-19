# Environment Setup

## Initial Setup
- Clone the repos (pull from someone's fork/branch if needed): [FCCeePhysicsPerformance](https://github.com/HEP-FCC/FCCeePhysicsPerformance) and [FCCAnalyses](https://github.com/HEP-FCC/FCCAnalyses)
- Start off in FCCeePhysicsPerformance to install Snakemake locally (hopefully it will get added to the FCC stack)
```bash
cd FCCeePhysicsPerformance/case-studies/flavour/tools
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
source install.sh $PWD/localPythonTools
```
- Now go to FCCAnalyses to pick up the FCC specific stuff
```bash
cd ../../../../FCCAnalyses/
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
```

## When starting up a new shell
- Pick up local packages such as Snakemake
```bash
cd FCCeePhysicsPerformance/case-studies/flavour/tools
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
source ./localSetup.sh $PWD/localPythonTools
```
- Pick up FCC software
```bash
cd ../../../../FCCAnalyses/
source ./setup.sh
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
```
<br />

# Running The Analysis
The final file of the workflow that depends on all possible steps is `./output/snakemake_flags/all` so request this from Snakemake if you want to run the entire analysis.

## To run the workflow locally
```bash
cd FCCAnalyses/examples/FCCee/flavour/b2snunu/
snakemake <target_output> -s ./scripts/Snakefile --jobs N --latency-wait 120
```

## To run the workflow on a Slurm cluster (deprecated method)
```bash
cd FCCAnalyses/examples/FCCee/flavour/b2snunu/
snakemake <target_output> -s ./scripts/Snakefile --jobs N --latency-wait 120 --cluster ./scripts/slurm_wrapper.py; mv ./slurm-* ./SlurmLogs
```
Other cluster types are possible but require a different wrapper, they aren't hard to make based off of our Slurm one.

## To run the workflow on a cluster (new method)
```bash
TODO
```
<br />

# What to do if something breaks
- Check if `master` has been updated in either FCCAnalyses or FCCeePhysicsPerformance as this may be related some deeper changes in the stack that are harder to track. Pulling these updates should hopefully fix things.