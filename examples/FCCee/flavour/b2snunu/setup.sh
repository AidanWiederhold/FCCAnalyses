echo "/cvmfs/sw.hsf.org/key4hep/releases/2024-04-12/x86_64-almalinux9-gcc11.3.1-opt/key4hep-stack/2024-04-12-bwtdjs/setup.sh" &> .fccana/stackpin
source setup.sh
python -m venv b2snunu_env
source ./b2snunu_env/bin/activate
pip install -r ./examples/FCCee/flavour/b2snunu/env.txt
fccanalysis build

export ANALYSISOUTPUT="/eos/experiment/fcc/ee/analyses_storage/flavor/b2snunu/revival/"
mkdir -p ${ANALYSISOUTPUT}logs
