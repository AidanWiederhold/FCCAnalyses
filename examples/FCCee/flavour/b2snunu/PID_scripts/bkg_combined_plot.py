import json
import matplotlib.pyplot as plt
import numpy as np
import config as cfg
import math
import matplotlib.patches as mpatches
from collections import Counter

sample_names = ["signal", *list(cfg.event_types.keys())][1:]

source_to_colour = {"signal": "green",
                    "p8_ee_Zbb_ecm91": "blue",
                    "p8_ee_Zcc_ecm91": "red",
                    "p8_ee_Zuds_ecm91": "orange"}

BF_scale = {"Bd2KstNuNu": 1e-5, # from https://arxiv.org/pdf/2201.07374.pdf
            "Bs2PhiNuNu": 1e-5}

def round_sf(x, sf=3):
    return round(x, sf-int(math.floor(math.log10(abs(x))))-1)

def latexify(decay_descriptor):
    new_desc = decay_descriptor
    if "gamma" in new_desc:
        new_desc.replace("gamma", "\gamma")
    return new_desc


def main(signal, bbbar, ccbar, qqbar, output_file, mva_cut, eos_cache, decay):

    with open("eos_cache.json") as inf:
        eos_cache = json.load(inf)

    total_events = {}
    for event_type in cfg.event_types.keys():
        samples = eos_cache[decay][event_type]["inclusive"]["samples"]
        total_samples = sum([len(sample) for sample in samples])
        total_events[event_type] = total_samples*cfg.events_per_file[decay][event_type]["inclusive"]
    samples = eos_cache[decay]["p8_ee_Zbb_ecm91"]["signal"]["samples"]
    total_samples = sum([len(sample) for sample in samples])
    total_events["signal"] = total_samples*cfg.events_per_file[decay]["p8_ee_Zbb_ecm91"]["signal"]

    print(total_events)

    combined_counts = {}
    for i, input_files in enumerate([signal, bbbar, ccbar, qqbar][1:]):
        for input_file in input_files:
            print(f"Input: {input_file}")
            with open(input_file, "r") as inf:
                decay_descriptors = json.load(inf)[mva_cut]
            for decay_descriptor, values in decay_descriptors.items():
                if "K- K+" in decay_descriptor:
                    decay_descriptor = decay_descriptor.replace("K- K+", "K+ K-")
                if "pi- pi+" in decay_descriptor:
                    decay_descriptor = decay_descriptor.replace("pi- pi+", "pi+ pi-")

                source = sample_names[i]
                if not decay_descriptor in combined_counts.keys():
                    combined_counts[decay_descriptor] = {}
                    combined_counts[decay_descriptor]["count"] = 0
                    combined_counts[decay_descriptor]["source"] = [source]
                #combined_counts[decay_descriptor]["count"] += values["count"]*(total_events["signal"]*cfg.branching_fractions[source])/total_events[source]
                combined_counts[decay_descriptor]["count"] += values["count"]
                combined_counts[decay_descriptor]["source"].append(source)
        

    ordered_decay_descriptors = []     
    for decay_desc, values in combined_counts.items():
        ordered_decay_descriptors.append([decay_desc, values["count"], values["source"]])
    ordered_decay_descriptors = sorted(ordered_decay_descriptors, key = lambda x: x[1], reverse=True)
    ordered_counts = {}
    for index, [decay_desc, count, source] in enumerate(ordered_decay_descriptors):
        if index<20:
            print(decay_desc, count)
            ordered_counts[decay_desc] = {}
            ordered_counts[decay_desc]["count"] = count
            #if source=="signal":
            #    ordered_counts[decay_desc]["count"] *= BF_scale[decay]
            #else:
            print(source)
            ordered_counts[decay_desc]["source"] = max(Counter(source))
        else:
            break

    for decay_desc, values in ordered_counts.items():
        print(decay_desc, values["count"])

    decay_descriptors = list(ordered_counts.keys())
    #decay_descriptors = [rf"{latexify(decay_descriptor)]
    y_pos = list(np.arange(len(ordered_counts.keys())))
    counts = [ordered_counts[decay_descriptor]["count"] for decay_descriptor in ordered_counts.keys()]
    #colours = [source_to_colour[ordered_counts[decay_descriptor]["source"]] for decay_descriptor in ordered_counts.keys()]
    y_pos.reverse()
    decay_descriptors.reverse()
    counts.reverse()

    fig, ax = plt.subplots()
    ax.barh(y_pos, counts, align="center")#, color=colours)
    # move desc to ticks
    #ax.set_yticks(y_pos, [f"{round_sf(count*100/total_events)}" for count in counts])
    #ax.set_yticks(y_pos, decay_descriptors)
    ax.set_yticks(y_pos, [i for i in range(1, len(decay_descriptors)+1)].reverse())
    #ax.set_xscale('log')
    ax.set_xlabel("Number of Events")
    ax.set_ylabel("Event Count Rank")
    #patches = [mpatches.Patch(color=source_to_colour[source], label=source) for source in source_to_colour.keys()]
    #ax.legend(handles=patches)
    for bar, decay in zip(ax.patches, decay_descriptors):
        ax.text(5., bar.get_y()+bar.get_height()/2, decay.replace("gamma", "g"), color = 'black', ha = 'left', va = 'center')
    fig.tight_layout()
    fig.set_size_inches(12,9)
    fig.savefig(args.output, dpi=400)



if __name__ == "__main__":
    # test with 
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inclusive_bbbar',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--inclusive_ccbar',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--inclusive_qqbar',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--signal',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    parser.add_argument('--mva_cut', type=str, required=True, help='Select the mva_cut.')
    parser.add_argument('--eos_cache', required=True, type=str, help='Select the output file.')
    parser.add_argument('--decay', required=True, type=str, help='Select the output file.')
    args = parser.parse_args()
    main(args.signal, args.inclusive_bbbar, args.inclusive_ccbar, args.inclusive_qqbar, args.output, args.mva_cut, args.eos_cache, args.decay)