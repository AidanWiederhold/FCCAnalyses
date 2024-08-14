# Setting the stage
Before you can safely run this code there is a small amount of editing to do.
In `/examples/FCCee/flavour/b2snunu/scripts/config.py` ensure that `outputDir` is set to a location you have read/write access to.

# initial setup do `source ./examples/FCCee/flavour/b2snunu/setup.sh` or
```bash
echo "/cvmfs/sw.hsf.org/key4hep/releases/2024-04-12/x86_64-almalinux9-gcc11.3.1-opt/key4hep-stack/2024-04-12-bwtdjs/setup.sh" &> .fccana/stackpin
source setup.sh
python -m venv b2snunu_env
source ./b2snunu_env/bin/activate
pip install -r ./examples/FCCee/flavour/b2snunu/env.txt
fccanalysis build

export ANALYSISOUTPUT="/eos/experiment/fcc/ee/analyses_storage/flavor/b2snunu/revival/"
mkdir -p ${ANALYSISOUTPUT}logs
```

The first line forces the `fccanalysis` pin to be the version this analysis was developed under.
To get a newer version you can simply skip that line and do `fccanalysis pin` after the `source setup.sh`.

# to activate the env do `source ./examples/FCCee/flavour/b2snunu/startup.sh` or
```bash
source setup.sh
source ./b2snunu_env/bin/activate

export ANALYSISOUTPUT="/eos/experiment/fcc/ee/analyses_storage/flavor/b2snunu/revival/"
mkdir -p ${ANALYSISOUTPUT}logs
```

# to apply changes to fccanalysis source code (in the FCCAnalyses directory)
```bash
fccanalysis build
```

# to run the analysis do `bash ./examples/FCCee/flavour/b2snunu/analysis.sh` or
```bash
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage1.py &> ./outputs/logs/stage1.log
```

# to test an `fccanalysis run` step do
```bash
fccanalysis run <analysis_script> --test &> ./outputs/logs/<analysis_stage>_test.log