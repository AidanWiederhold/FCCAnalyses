source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
#source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2023-01-15/x86_64-centos7-gcc11.2.0-opt/csapx/setup.sh
cd FCCeePhysicsPerformance/case-studies/flavour/tools
source install.sh $PWD/localPythonTools
source localSetup.sh $PWD/localPythonTools
cd ../../../../FCCAnalyses/
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ../
cd ../
#pip3 install --user xgboost #hopefully I can get this to work in the initial setup
