cd FCCAnalyses
#source setup.sh
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2023-01-15/x86_64-centos7-gcc11.2.0-opt/csapx/setup.sh
fccanalysis build
cd ./examples/FCCee/flavour/b2snunu
source ./pippa.sh $PWD/localPythonTools