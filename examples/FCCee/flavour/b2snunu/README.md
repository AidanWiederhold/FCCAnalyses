# initial setup
```bash
source setup.sh
fccanalysis pin
python -m venv b2snunu_env
source ./b2snunu_env/bin/activate
pip install -r ./examples/FCCee/flavour/b2snunu/env.txt
fccanalysis build
```

# activating the setup env
```bash
source setup.sh
source ./b2snunu_env/bin/activate.txt
```

# to apply changes to fccanalysis source code (in the FCCAnalyses directory)
```bash
fccanalysis build
```

# to run the analysis (inside the `/examples/FCCee/flavour/b2snunu/` directory)
```bash
snakemake output/snakemake_flags/all -s scripts/Snakefile --latency-wait 120 --jobs 100 --cluster <cluster_wrapper>
```