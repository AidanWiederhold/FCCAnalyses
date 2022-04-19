analysis_scripts = "scripts/"
outputs = "output/"
snakemake_flags = f"{outputs}snakemake_flags/"
logs = f"logs/"
benchmarks = f"benchmarks/"
input_mc = f"{outputs}/input_mc/"

MC = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/"

event_types = {
    "p8_ee_Zbb_ecm91": ["inclusive", "signal"],
    "p8_ee_Zcc_ecm91": ["inclusive"],
    "p8_ee_Zuds_ecm91": ["inclusive"],
}
decays = ["Bd2KstNuNu", "Bs2PhiNuNu"]#, "Bu2KNuNu"]
samples = set()

decay_to_candidates = {
    "Bd2KstNuNu": "KPi",
    "Bs2PhiNuNu": "KK", # TODO check this https://pdglive.lbl.gov/Particle.action?init=0&node=M004&home=MXXX005
    "Bu2KNuNu": "K",
}

decay_to_pdgids = {
    "Bd2KstNuNu": ["313", "511"],
    "Bs2PhiNuNu": ["333", "531"],
    "Bu2KNuNu": ["321", "521"],
}

tuple_id_blacklist = {
    "Bd2KstNuNu": {
        "p8_ee_Zbb_ecm91": {
            "inclusive": ["255", "230"],
            "signal": [],
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": [],
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": [],
        },
    },
    "Bs2PhiNuNu": {
        "p8_ee_Zbb_ecm91": {
            "inclusive": ["255", "230"],
            "signal": [],
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": [],
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": [],
        },
    },
    "Bu2KNuNu": {
        "p8_ee_Zbb_ecm91": {
            "inclusive": ["255", "230"],
            "signal": [],
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": [],
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": [],
        },
    },
}

def blacklister(tuple_ids, blacklist):
    return [tuple_id for tuple_id in tuple_ids if str(tuple_id) not in blacklist]


def decays_to_fnames(decays):
    return [f"_EvtGen_{decay}" if decay!="inclusive" else "" for decay in decays]

def decay_model_to_fname(decay_model, decay):
    if decay_model=="signal":
        return decays_to_fnames([decay])[0]
    else:
        return decays_to_fnames([decay_model])[0]

def list_to_constraints(l):
    constraints = f"({l[0]}"
    for item in l[1:]:
        constraints = f"{constraints}|{item}"
    constraints = f"{constraints})"
    return constraints