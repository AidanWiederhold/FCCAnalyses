# with the current environment set up snakemake cannot be imported so need to just run this bit in a separate conda environment
# TODO fix that

def replace_PID(samples, PID):
    #print(samples)
    samples = [sample.replace("0p0", PID) for sample in samples]
    #print(samples)
    return samples

def cache(outf_name, sample_portion, group_size):
    from snakemake.remote.XRootD import RemoteProvider as XRootDRemoteProvider
    XRootD = XRootDRemoteProvider(stay_on_remote=True)
    import json
    from config import MC, event_types, decay_model_to_fname, decays, outputs, training_proportions
    from pathlib import Path
    import math
    import random

    random.seed(980608)

    eos_cache = {}

    print("Starting EOS querying!")
    for decay in decays:
        eos_cache[decay] = {}
        for event_type, decay_models in event_types.items():
            eos_cache[decay][event_type] = {}
            for decay_model in decay_models:
                if decay=="Bd2KsNuNu" and decay_model == "signal":
                    _group_size = max(int(group_size/10.), 1)
                else:
                    _group_size = group_size
                eos_cache[decay][event_type][decay_model] = {}
                eos_cache[decay][event_type][decay_model]["samples"] = {}
                eos_cache[decay][event_type][decay_model]["expected_output"] = {}
                eos_cache[decay][event_type][decay_model]["expected_output_ids"] = {}
                eos_cache[decay][event_type][decay_model]["training_output"] = {}
                eos_cache[decay][event_type][decay_model]["training_output_ids"] = {}
                eos_cache[decay][event_type][decay_model]["training"] = {}
                path = MC+f"{event_type}{decay_model_to_fname(decay_model, decay)}"
                result = XRootD.glob_wildcards(path+"/events_{sample}.root")
                result = result[0][0:int(len(result[0])*sample_portion)]
                eos_cache[decay][event_type][decay_model]["samples"]["0p0"]=[]
                for i in range(1, max(math.floor(len(result)/_group_size),1)+1):
                    eos_cache[decay][event_type][decay_model]["samples"]["0p0"].append(result[(i-1)*_group_size:i*_group_size])
                if result[i*_group_size:-1]!=[]:
                    eos_cache[decay][event_type][decay_model]["samples"]["0p0"].append(result[i*_group_size:-1])
                eos_cache[decay][event_type][decay_model]["expected_output"]["0p0"] = [f"{outputs}root/0p0/stage1/{decay}/{event_type}/{decay_model}/{i}.root" for i in range(len(eos_cache[decay][event_type][decay_model]["samples"]["0p0"]))]
                eos_cache[decay][event_type][decay_model]["expected_output_ids"]["0p0"] = [i for i in range(len(eos_cache[decay][event_type][decay_model]["samples"]["0p0"]))]
                
                training_portion = training_proportions[decay][event_type][decay_model]
                total_samples = len(eos_cache[decay][event_type][decay_model]["samples"]["0p0"])
                eos_cache[decay][event_type][decay_model]["training"]["0p0"] = random.sample(eos_cache[decay][event_type][decay_model]["samples"]["0p0"], int(total_samples*training_portion))
                eos_cache[decay][event_type][decay_model]["training_output"]["0p0"] = []
                eos_cache[decay][event_type][decay_model]["training_output_ids"]["0p0"] = []
                print(f"For {decay} the {event_type} {decay_model} BDT 1 training will feature {_group_size*int(total_samples*training_portion)} input files!")
                for sample_group in eos_cache[decay][event_type][decay_model]["training"]["0p0"]:
                    index = eos_cache[decay][event_type][decay_model]["samples"]["0p0"].index(sample_group)
                    output_name = eos_cache[decay][event_type][decay_model]["expected_output"]["0p0"][index].replace("stage1", "training")
                    eos_cache[decay][event_type][decay_model]["training_output"]["0p0"].append(output_name)
                    eos_cache[decay][event_type][decay_model]["training_output_ids"]["0p0"].append(eos_cache[decay][event_type][decay_model]["expected_output_ids"]["0p0"][index])
                    eos_cache[decay][event_type][decay_model]["samples"]["0p0"].remove(eos_cache[decay][event_type][decay_model]["samples"]["0p0"][index])
                    eos_cache[decay][event_type][decay_model]["expected_output"]["0p0"].remove(eos_cache[decay][event_type][decay_model]["expected_output"]["0p0"][index])
                    eos_cache[decay][event_type][decay_model]["expected_output_ids"]["0p0"].remove(eos_cache[decay][event_type][decay_model]["expected_output_ids"]["0p0"][index])

                    
                PID_seps = [PID_sep for PID_sep in cfg.PID_seps if PID_sep!="0p0"]
                for PID_sep in PID_seps:
                    n_seps = len(PID_seps)
                    eos_cache[decay][event_type][decay_model]["training"][PID_sep] = eos_cache[decay][event_type][decay_model]["training"]["0p0"]
                    if PID_sep in eos_cache[decay][event_type][decay_model]["training_output"].keys():
                        print("before", decay, event_type, decay_model, PID_sep, eos_cache[decay][event_type][decay_model]["training_output"][PID_sep])
                    eos_cache[decay][event_type][decay_model]["training_output"][PID_sep] = replace_PID(eos_cache[decay][event_type][decay_model]["training_output"]["0p0"], PID_sep)
                    print(decay, event_type, decay_model, PID_sep, eos_cache[decay][event_type][decay_model]["training_output"][PID_sep])
                    eos_cache[decay][event_type][decay_model]["training_output_ids"][PID_sep] = eos_cache[decay][event_type][decay_model]["training_output_ids"]["0p0"]
                    n_entries = len(eos_cache[decay][event_type][decay_model]["samples"]["0p0"])
                    eos_cache[decay][event_type][decay_model]["samples"][PID_sep] = eos_cache[decay][event_type][decay_model]["samples"]["0p0"][:int(max((n_entries/n_seps), 1))]
                    n_entries = len(eos_cache[decay][event_type][decay_model]["expected_output"]["0p0"])
                    eos_cache[decay][event_type][decay_model]["expected_output"][PID_sep] = replace_PID(eos_cache[decay][event_type][decay_model]["expected_output"]["0p0"][:int(max((n_entries/n_seps), 1))], PID_sep)
                    n_entries = len(eos_cache[decay][event_type][decay_model]["expected_output_ids"]["0p0"])
                    eos_cache[decay][event_type][decay_model]["expected_output_ids"][PID_sep] = eos_cache[decay][event_type][decay_model]["expected_output_ids"]["0p0"][:int(max((n_entries/n_seps), 1))]
                    
        print(f"Finished {decay}!")

    for decay in decays:
        for event_type, decay_models in event_types.items():
            for decay_model in decay_models:
                for data_type, PID_sep in eos_cache[decay][event_type][decay_model].items():
                    if data_type=="training_output":
                        for PID_sep, entries in PID_sep.items():
                            print(entries)

    if not Path(outputs).exists():
        Path(outputs).mkdir()
    with open(outf_name, 'w', encoding='utf-8') as f:
        json.dump(eos_cache, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--sample_portion', default = 1., type=float, help='Choose the fraction of MC to use.')
    parser.add_argument('--group_size', default = 20, type=int, help='Choose how many MC samples to group together for processing to reduce the total number of files in the workflow.')
    args = parser.parse_args()
    import config as cfg
    cache(cfg.eos_cache, args.sample_portion, args.group_size)

