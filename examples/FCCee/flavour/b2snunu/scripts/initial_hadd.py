import argparse
import subprocess
import json
from config import MC, decays_to_fnames

parser = argparse.ArgumentParser(description="Hadds FCC MC to reduce the number of input files for Snakemake to check for", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--eos_cache', type=str, required=True, help='Select the input file.')
args = parser.parse_args()

with open(args.eos_cache) as inf:
    eos_cache = json.load(inf)

total_jobs = 0
for _event_type, _decays in eos_cache.items():
    for _decay, _decay_info in _decays.items():
        total_jobs+=len(_decay_info["expected_output"])

counter = 0
for _event_type, _decays in eos_cache.items():
    for _decay, _decay_info in _decays.items():
        input_location = f"{MC}{_event_type}{decays_to_fnames([_decay])[0]}/events_"
        for i, tuple_group in enumerate(_decay_info["samples"]):
            cmd = f"hadd -fk {_decay_info['expected_output'][i]}"
            for inf_id in tuple_group:
                cmd = f"{cmd} {input_location}{inf_id}.root"
            print(f"Executing: {cmd}")
            if counter==0:
                subprocess.run(cmd)
            else:
                break
            counter+=1
            print(f"Job {counter} of {total_jobs} completed!")

