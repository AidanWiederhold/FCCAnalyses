# with the current environment set up snakemake cannot be imported so need to just run this bit in a separate conda environment
# TODO fix that

def cache(outf_name, sample_portion, group_size=20):
    from snakemake.remote.XRootD import RemoteProvider as XRootDRemoteProvider
    XRootD = XRootDRemoteProvider(stay_on_remote=True)
    import json
    from config import MC, event_types, decay_model_to_fname, decays
    from pathlib import Path
    import math

    eos_cache = {}

    #total_queries = 0
    #for event_type, info in event_types.items():
    #    total_queries+=len(info["decays"])

    print("Starting EOS querying!")
    #counter=0
    for decay in decays:
        eos_cache[decay] = {}
        for event_type, decay_models in event_types.items():
            eos_cache[decay][event_type] = {}
            for decay_model in decay_models:
                eos_cache[decay][event_type][decay_model] = {}
                path = MC+f"{event_type}{decay_model_to_fname(decay_model, decay)}"
                result = XRootD.glob_wildcards(path+"/events_{sample}.root")
                result = result[0][0:int(len(result[0])*sample_portion)]
                eos_cache[decay][event_type][decay_model]["samples"]=[]
                for i in range(1, max(math.floor(len(result)/group_size),1)+1):
                    eos_cache[decay][event_type][decay_model]["samples"].append(result[(i-1)*group_size:i*group_size])
                if result[i*group_size:-1]!=[]:
                    eos_cache[decay][event_type][decay_model]["samples"].append(result[i*group_size:-1])
                #print(f"Queried {counter} of {total_queries} directories",end="\r")
                eos_cache[decay][event_type][decay_model]["expected_output"] = [f"{outputs}stage1/{decay}/{event_type}/{decay_model}/{i}.root" for i in range(len(eos_cache[decay][event_type][decay_model]["samples"]))]
        print(f"\nFinished!")

    if not Path(outputs).exists():
        Path(outputs).mkdir()
    with open(outf_name, 'w', encoding='utf-8') as f:
        json.dump(eos_cache, f, ensure_ascii=False, indent=4)

    return eos_cache

if __name__ == "__main__":
    import sys
    from config import outputs
    if len(sys.argv)>1:
        sample_portion = float(sys.argv[1])
    else:
        sample_portion = 1.
    sample_portion
    cache(f"eos_cache.json", sample_portion)

