cd FCCeePhysicsPerformance/case-studies/flavour/tools
#source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2023-01-15/x86_64-centos7-gcc11.2.0-opt/csapx/setup.sh
source ./localSetup.sh $PWD/localPythonTools
cd ../../../../FCCAnalyses/
source ./setup.sh
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ../../FCCAnalyses/examples/FCCee/flavour/b2snunu/

#source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2023-01-15/x86_64-centos7-gcc11.2.0-opt/csapx/setup.sh
#source ./venv/bin/activate
#cd ./FCC/FCCAnalyses/examples/FCCee/flavour/b2snunu/
