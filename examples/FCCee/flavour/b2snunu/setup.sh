cd FCCeePhysicsPerformance/case-studies/flavour/tools
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
source install.sh $PWD/localPythonTools
cd ../../../../FCCAnalyses/
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install