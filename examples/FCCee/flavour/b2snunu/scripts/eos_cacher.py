# with the current environment set up snakemake cannot be imported so need to use conda before source the FCC environment
# TODO fix that

def cache(outf_name, sample_portion):
    from snakemake.remote.XRootD import RemoteProvider as XRootDRemoteProvider
    XRootD = XRootDRemoteProvider(stay_on_remote=True)
    import json
    from config import MC, event_types, decays_to_fnames
    from pathlib import Path
    import math

    eos_cache = {}

    total_queries = 0
    for event_type, info in event_types.items():
        total_queries+=len(info["decays"])

    print("Starting EOS querying!")
    counter=0
    for i, event_type in enumerate(event_types.keys()):
        eos_cache[event_type] = {}
        for j, decay in enumerate(event_types[event_type]["decays"]):
            counter+=1
            eos_cache[event_type][decay] = {}
            path = MC+f"{event_type}{decays_to_fnames([decay])[0]}"
            result = XRootD.glob_wildcards(path+"/events_{sample}.root")
            result = result[0][0:int(len(result[0])*sample_portion)]
            eos_cache[event_type][decay]["samples"]=[]
            # choose groups of 80 tuples to make the output about 4GB each
            for i in range(1, math.floor(len(result)/80)+1):
                eos_cache[event_type][decay]["samples"].append(result[(i-1)*80:i*80])
            eos_cache[event_type][decay]["samples"].append(result[i*80:-1])
            print(f"Queried {counter} of {total_queries} directories",end="\r")
            eos_cache[event_type][decay]["expected_output"] = [f"{outputs}/mc/{event_type}/{decay}/{i}.root" for i in range(len(eos_cache[event_type][decay]["samples"]))]
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
    cache(f"{outputs}eos_cache.json", sample_portion)

