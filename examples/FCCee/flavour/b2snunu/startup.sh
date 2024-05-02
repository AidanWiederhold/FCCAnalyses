# use in FCCAnalyses
cd ./examples/FCCee/flavour/b2snunu
export COMMON=$PWD/python
export PATH=$PWD/localPythonTools/.local/bin:$PATH
export PYTHONPATH=$PWD/localPythonTools/.local/lib/python3.9/site-packages:$COMMON:$PYTHONPATH
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2023-01-15/x86_64-centos7-gcc11.2.0-opt/csapx/setup.sh
cd ../../../../build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ../../FCCAnalyses/examples/FCCee/flavour/b2snunu/