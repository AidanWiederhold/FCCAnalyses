#source setup.sh
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2023-01-15/x86_64-centos7-gcc11.2.0-opt/csapx/setup.sh

#fccanalysis build

#export LOCAL_DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd)
export LOCAL_DIR=$PWD
#echo $LOCAL_DIR

export PYTHONPATH=${LOCAL_DIR}:${PYTHONPATH}
export PYTHONPATH=${LOCAL_DIR}/python:${PYTHONPATH}
export PATH=${LOCAL_DIR}/bin:${PATH}
export LD_LIBRARY_PATH=${LOCAL_DIR}/install/lib:${LD_LIBRARY_PATH}
export CMAKE_PREFIX_PATH=${LOCAL_DIR}/install:${CMAKE_PREFIX_PATH}
export ROOT_INCLUDE_PATH=${LOCAL_DIR}/install/include:${ROOT_INCLUDE_PATH}

export ONNXRUNTIME_ROOT_DIR=`python -c "import onnxruntime; print(onnxruntime.__path__[0]+'/../../../..')"`
export LD_LIBRARY_PATH=$ONNXRUNTIME_ROOT_DIR/lib:$LD_LIBRARY_PATH
mkdir build install
cd build 
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ../../FCCAnalyses/examples/FCCee/flavour/b2snunu/

#cd ./examples/FCCee/flavour/b2snunu
source ./pippa.sh $PWD/localPythonTools