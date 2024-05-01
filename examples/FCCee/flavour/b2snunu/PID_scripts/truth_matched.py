import uproot
from particle import Particle
import json
from config import MVA_cuts, decay_to_candidates, truth_ids
import copy
    

def main(input_file, decay, target_ids, output_file):
    bkg_branches = [f"{candidate}Candidates_truth",
                    "MC_PDG",
                    "MC_M1",
                    "MC_M2",
                    "MC_D1",
                    "MC_D2",
                    "MC_D3",
                    "MC_D4",
                    ]
    with uproot.open(input_file) as inf:
        arr = inf.arrays(entry_stop=100)
    n_events = len(arr)
    truth_info = []
    for event_index, event in enumerate(arr[f"{candidate}Candidates_truth"]):
        #print(f"{100*event_index/n_events:.2f} % of events determined", end="\r")
        truth_matched_candidates = []
        for candidate_index in event:
            truth_matched = 0
            if candidate_index!=-999: # TODO what to do with events where the candidate index is -999? Could try find some particle that does have an index and grow the tree from there
                candidate_id = arr["MC_PDG"][event_index][candidate_index]
                parent_index = arr["MC_M1"][event_index][candidate_index]
                if parent_index != -999:
                    parent_id = arr["MC_PDG"][event_index][parent_index]
                    sibling_indices = [arr[f"MC_D{i}"][event_index][parent_index] for i in range(1,5)]
                    if candidate_index in sibling_indices: # TODO investigate why this can sometimes not happen and figure out if we should be concerned
                        sibling_indices.remove(candidate_index)
                    sibling_ids = [arr["MC_PDG"][event_index][sibling_index] for sibling_index in sibling_indices if sibling_index!=-999]
                    sibling_ids.sort()
                else:
                    parent_id = -999
                    sibling_ids = [-999]
                children_indices = [arr[f"MC_D{i}"][event_index][candidate_index] for i in range(1,5)]
                children_ids = [arr["MC_PDG"][event_index][child_index] for child_index in children_indices if child_index!=-999]

                if abs(parent_id) == target_ids["parent"]:
                    sign = parent_id/abs(parent_id)
                    if sign<0:
                        children_ids = [-pdgid for pdgid in children_ids]
                    children_ids.sort()
                    if sign*candidate_id == target_ids["candidate"] and children_ids == target_ids["children"]:
                        for possible_siblings in target_ids["siblings"]:
                            if sibling_ids==possible_siblings:
                                truth_matched = 1
                                break
                truth_matched_candidates.append(truth_matched)
                if truth_matched==1 and not ((parent_id==-511.0 and candidate_id==-313.0  and sibling_ids==[-12.0, 12.0] and children_ids==[-211.0, 321.0]) or (parent_id==511.0 and candidate_id==313.0  and sibling_ids==[-12.0, 12.0] and children_ids==[-211.0, 321.0])):
                    print(truth_matched, parent_id, candidate_id, sibling_ids, children_ids, sign)
                    raise RuntimeError("check above")
        truth_info.append(truth_matched_candidates)
    new_arr
                        # to output could try just pickling it https://github.com/matthewkenzie/FCCAnalyses/blob/knunu_attempts/examples/FCCee/flavour/Bd2KstNuNu/run_truth_match.py




if __name__ == "__main__":
    # test with `python ./scripts/bkg_matching.py --input_files ./p8_ee_Zbb_Bd2KstNuNu_stage1.root:events --output_file ./decay_trees.json`
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input_files',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--tree_name', type=str, required=True, help='Select the input tree.')
    parser.add_argument('--decay', type=str, required=True, help='Select the decay.')
    parser.add_argument('--output_file', required=True, type=str, help='Select the output file.')
    args = parser.parse_args()
    candidate = decay_to_candidates[args.decay]
    target_ids = truth_ids[args.decay]
    input_files = [f"{file}:{args.tree_name}" for file in args.input_files]
    main(input_files, candidate, target_ids, args.output_file)