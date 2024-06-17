source setup.sh
fccanalysis pin
python -m venv b2snunu_env
source ./b2snunu_env/bin/activate
pip install -r ./examples/FCCee/flavour/b2snunu/env.txt
fccanalysis build
mkdir -p ./outputs/logs