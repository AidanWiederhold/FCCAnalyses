analysis_scripts = "scripts/"
outputs = "output/"
snakemake_flags = f"{outputs}snakemake_flags/"
logs = f"logs/"
benchmarks = f"benchmarks/"
input_mc = f"{outputs}/input_mc/"

MC = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/"

event_types = {
    "p8_ee_Zbb_ecm91": {"decays": ["inclusive", "Bd2KstNuNu"]},
    #"p8_ee_Zcc_ecm91": {"decays": ["inclusive"]},
    #"p8_ee_Zuds_ecm91": {"decays": ["inclusive"]},
}
decays = set()
samples = set()
for event_type, info in event_types.items():
    decays.update(info["decays"])

def decays_to_fnames(decays):
    return [f"_EvtGen_{decay}" if decay!="inclusive" else "" for decay in decays]

def list_to_constraints(l):
    constraints = f"({l[0]}"
    for item in l[1:]:
        constraints = f"{constraints}|{item}"
    constraints = f"{constraints})"
    return constraints