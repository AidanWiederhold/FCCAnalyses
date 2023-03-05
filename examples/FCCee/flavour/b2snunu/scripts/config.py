analysis_scripts = "scripts/"
outputs = "output_new_var/"
plots = f"{outputs}plots/"
snakemake_flags = f"{outputs}snakemake_flags/"
logs = f"logs_new_var/"
benchmarks = f"benchmarks_new_var/"
input_mc = f"{outputs}/input_mc/"
envs = "../envs/"
eos_cache = "eos_cache_new_var.json"

MC = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/"

event_types = {
    "p8_ee_Zbb_ecm91": ["inclusive", "signal"],
    "p8_ee_Zcc_ecm91": ["inclusive"],
    "p8_ee_Zuds_ecm91": ["inclusive"],
}
decays = ["Bd2KstNuNu", "Bs2PhiNuNu", "Bd2KsNuNu", "Lb2LbNuNu"]#, "Bu2KNuNu"]
#decays = ["Bd2KsNuNu", "Lb2LbNuNu"]
samples = set()

label_map = { 'p8_ee_Zbb_ecm91': r'$Z\to b\bar{b}$',
              'p8_ee_Zcc_ecm91': r'$Z\to c\bar{c}$',
              'p8_ee_Zuds_ecm91': r'$Z\to q\bar{q}$'
            }


decay_to_candidates = {
    "Bd2KstNuNu": "KPi",
    "Bs2PhiNuNu": "KK",
    #"Bu2KNuNu": "K",
    "Bd2KsNuNu": "PiPi",
    "Lb2LbNuNu": "pPi"
}

decay_to_pdgids = {
    "Bd2KstNuNu": ["313", "511"],
    "Bs2PhiNuNu": ["333", "531"],
    #"Bu2KNuNu": ["321", "521"],
    "Bd2KsNuNu": ["310", "511"],
    "Lb2LbNuNu": ["3122", "5122"],
}

# rough estimate from running a few files
stage1_efficiencies = {
    "Bd2KstNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 0.82,
            "inclusive": 0.19,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 0.15,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 0.0047,
        },
    },
    "Bs2PhiNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 0.84,
            "inclusive": 0.017,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 0.013,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 0.00051,
        },
    },
    "Bd2KsNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 164828./200000.,
            "inclusive": 755455./2000000.,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 665845./2000000.,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 367748./2000000.,
        },
    },
    "Lb2LbNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 150101./200000.,
            "inclusive": 86385./2000000.,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 89519./2000000.,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 107630./2000000.,
        },
    },
   # "Bu2KNuNu": {
   #     "p8_ee_Zbb_ecm91": {
   #         "signal": 171835./200000.,
   #         "inclusive": 35289./2000000.,
   #     },
   #     "p8_ee_Zcc_ecm91": {
   #         "inclusive": 25415./2000000.,
   #     },
   #     "p8_ee_Zuds_ecm91": {
   #         "inclusive": 1046./2000000.,
   #     },
   # },
}

branching_fractions = {
    "signal": 0.1512,
    "p8_ee_Zbb_ecm91": 0.1512,
    "p8_ee_Zcc_ecm91": 0.1203,
    "p8_ee_Zuds_ecm91": 0.6991-0.1512-0.1203,
}

training_proportions = {
    "Bd2KstNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 140/1000,
            "inclusive": 40/10000,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 40/10000,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 100/10000,
        },
    },
    "Bs2PhiNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 120/1000,
            "inclusive": 360/10000,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 280/10000,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 1000/10000,
        },
    },
    "Bd2KsNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 14/100,
            "inclusive": 20/10000,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 20/10000,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 40/10000,
        },
    },
    "Lb2LbNuNu": {
        "p8_ee_Zbb_ecm91": {
            "signal": 140/1000,
            "inclusive": 60/10000,
        },
        "p8_ee_Zcc_ecm91": {
            "inclusive": 40/10000,
        },
        "p8_ee_Zuds_ecm91": {
            "inclusive": 140/10000,
        },
    }
    #"Bu2KNuNu": {
    #    "p8_ee_Zbb_ecm91": {
    #        "signal": 120/1000,
    #        "inclusive": 400/10000,
    #    },
    #    "p8_ee_Zcc_ecm91": {
    #        "inclusive": 300/10000,
    #    },
    #    "p8_ee_Zuds_ecm91": {
    #        "inclusive": 1000/10000,
    #    },
    #},
}

events_per_file = {}
for decay in decays:
    events_per_file[decay] = {
                            "p8_ee_Zbb_ecm91": {
                                "signal": 10000,
                                "inclusive": 100000,
                            },
                            "p8_ee_Zcc_ecm91": {
                                "inclusive": 100000,
                            },
                            "p8_ee_Zuds_ecm91": {
                                "inclusive": 100000,
                            }
    }

events_per_file["Lb2LbNuNu"] = {
                            "p8_ee_Zbb_ecm91": {
                                "signal": 100000,
                                "inclusive": 100000,
                            },
                            "p8_ee_Zcc_ecm91": {
                                "inclusive": 100000,
                            },
                            "p8_ee_Zuds_ecm91": {
                                "inclusive": 100000,
                            }
    }

tuple_id_blacklist = {} # TODO should probably report broken MC
for decay in decays:
    tuple_id_blacklist[decay] = {
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
    }

MVA_cuts = [0.6, 0.7, 0.8, 0.9, 0.99]

mass_cut = {"KPi": [0.65, 1.1],
            "KK": [1., 1.06],
            "PiPi": [0.45, 0.55],
            "pPi": [1.1, 1.13],}

KPi_cut = f"((KPiCandidates_mass[0]>{mass_cut['KPi'][0]} && KPiCandidates_mass[0]<{mass_cut['KPi'][1]})"
KK_cut = f"((KKCandidates_mass[0]>{mass_cut['KK'][0]} && KKCandidates_mass[0]<{mass_cut['KK'][1]})"
PiPi_cut = f"((PiPiCandidates_mass[0]>{mass_cut['PiPi'][0]} && PiPiCandidates_mass[0]<{mass_cut['PiPi'][1]})"
pPi_cut = f"((pPiCandidates_mass[0]>{mass_cut['pPi'][0]} && pPiCandidates_mass[0]<{mass_cut['pPi'][1]})"
for i in range(1,10):
    KPi_cut = f"{KPi_cut} || (KPiCandidates_mass[{i}]>{mass_cut['KPi'][0]} && KPiCandidates_mass[{i}]<{mass_cut['KPi'][1]})"
    KK_cut = f"{KK_cut} || (KKCandidates_mass[{i}]>{mass_cut['KK'][0]} && KKCandidates_mass[{i}]<{mass_cut['KK'][1]})"
    PiPi_cut = f"{PiPi_cut} || (PiPiCandidates_mass[{i}]>{mass_cut['PiPi'][0]} && PiPiCandidates_mass[{i}]<{mass_cut['PiPi'][1]})"
    pPi_cut = f"{pPi_cut} || (pPiCandidates_mass[{i}]>{mass_cut['pPi'][0]} && pPiCandidates_mass[{i}]<{mass_cut['pPi'][1]})"
KPi_cut = f"{KPi_cut})"
KK_cut = f"{KK_cut})"
PiPi_cut = f"{PiPi_cut})"
pPi_cut = f"{pPi_cut})"
mass_cuts = {"Bd2KstNuNu": KPi_cut,
             "Bs2PhiNuNu": KK_cut,
             "Bd2KsNuNu": PiPi_cut,
             "Lb2LbNuNu": pPi_cut
            }

truth_ids = {"Bd2KstNuNu": {"parent": 511,
                            "candidate": 313,
                            "children": [-211, 321],
                            "siblings": [[-12, 12], [-14, 14], [-16, 16]],
                            },
             "Bs2PhiNuNu": {"parent": 531,
                            "candidate": 333,
                            "children": [-321, 321],
                            "siblings": [[-12, 12], [-14, 14], [-16, 16]],
                            },
             "Bd2KsNuNu": {"parent": 511,
                            "candidate": 310,
                            "children": [-211, 211],
                            "siblings": [[-12, 12], [-14, 14], [-16, 16]],
                            },
             "Lb2LbNuNu": {"parent": 5122,
                            "candidate": 3122,
                            "children": [2212, -211],
                            "siblings": [[-12, 12], [-14, 14], [-16, 16]],
                            },
            }

def stage1_branches(candidates):
    return [
            "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2","MC_D3","MC_D4",
            "MC_p","MC_pt","MC_px","MC_py","MC_pz","MC_eta","MC_phi",
            "MC_orivtx_x","MC_orivtx_y","MC_orivtx_z",
            "MC_endvtx_x", "MC_endvtx_y", "MC_endvtx_z", "MC_e","MC_m",
            "EVT_ThrustEmin_E",          "EVT_ThrustEmax_E",
            "EVT_ThrustEmin_Echarged",   "EVT_ThrustEmax_Echarged",
            "EVT_ThrustEmin_Eneutral",   "EVT_ThrustEmax_Eneutral",
            "EVT_ThrustEmin_N",          "EVT_ThrustEmax_N",
            "EVT_ThrustEmin_Ncharged",   "EVT_ThrustEmax_Ncharged",
            "EVT_ThrustEmin_Nneutral",   "EVT_ThrustEmax_Nneutral",
            "EVT_ThrustEmin_NDV",        "EVT_ThrustEmax_NDV",
            "EVT_Thrust_Mag",
            "EVT_Thrust_X",  "EVT_Thrust_XErr",
            "EVT_Thrust_Y",  "EVT_Thrust_YErr",
            "EVT_Thrust_Z",  "EVT_Thrust_ZErr",

            "EVT_NtracksPV", "EVT_NVertex", f"EVT_N{candidates}",

            "EVT_dPV2DVmin","EVT_dPV2DVmax","EVT_dPV2DVave",

            "MC_Vertex_x", "MC_Vertex_y", "MC_Vertex_z",
            "MC_Vertex_ntrk", "MC_Vertex_n",

            "MC_Vertex_PDG","MC_Vertex_PDGmother","MC_Vertex_PDGgmother",

            "Vertex_x", "Vertex_y", "Vertex_z",
            "Vertex_xErr", "Vertex_yErr", "Vertex_zErr",
            "Vertex_isPV", "Vertex_ntrk", "Vertex_chi2", "Vertex_n",
            "Vertex_thrust_angle", "Vertex_thrusthemis_emin", "Vertex_thrusthemis_emax",

            "Vertex_d2PV", "Vertex_d2PVx", "Vertex_d2PVy", "Vertex_d2PVz",
            "Vertex_d2PVErr", "Vertex_d2PVxErr", "Vertex_d2PVyErr", "Vertex_d2PVzErr",
            "Vertex_mass",
            "DV_d0","DV_z0",

            f"True{candidates}_vertex", f"True{candidates}_d0", f"True{candidates}_z0",

            f"{candidates}Candidates_mass", f"{candidates}Candidates_vertex", f"{candidates}Candidates_mcvertex", f"{candidates}Candidates_B",
            f"{candidates}Candidates_truth",
            f"{candidates}Candidates_px", f"{candidates}Candidates_py", f"{candidates}Candidates_pz", f"{candidates}Candidates_p", f"{candidates}Candidates_q",
            f"{candidates}Candidates_d0",  f"{candidates}Candidates_z0",f"{candidates}Candidates_anglethrust",

            f"{candidates}Candidates_h1px", f"{candidates}Candidates_h1py", f"{candidates}Candidates_h1pz",
            f"{candidates}Candidates_h1p", f"{candidates}Candidates_h1q", f"{candidates}Candidates_h1m", f"{candidates}Candidates_h1type",
            f"{candidates}Candidates_h1d0", f"{candidates}Candidates_h1z0",
            f"{candidates}Candidates_h2px", f"{candidates}Candidates_h2py", f"{candidates}Candidates_h2pz",
            f"{candidates}Candidates_h2p", f"{candidates}Candidates_h2q", f"{candidates}Candidates_h2m", f"{candidates}Candidates_h2type",
            f"{candidates}Candidates_h2d0", f"{candidates}Candidates_h2z0",
            ]

def check_blacklist(target, blacklist, mode="file_name"):
    if mode=="file_name":
        for entry in blacklist:
            if f"/{entry}." in target:
                return True
        return False
    else:
        if str(target) in blacklist:
            return True
        else:
            return False

def blacklister(tuple_ids, blacklist, mode="file_name"):
    if mode=="file_name":
        return [tuple_id for tuple_id in tuple_ids if not check_blacklist(str(tuple_id), blacklist)]
    else:
        return [tuple_id for tuple_id in tuple_ids if not check_blacklist(str(tuple_id), blacklist, mode="id")]

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

#First stage BDT including event-level vars
train_vars = ["EVT_ThrustEmin_E",
              "EVT_ThrustEmax_E",
              "EVT_ThrustEmin_Echarged",
              "EVT_ThrustEmax_Echarged",
              "EVT_ThrustEmin_Eneutral",
              "EVT_ThrustEmax_Eneutral",
              "EVT_ThrustEmin_Ncharged",
              "EVT_ThrustEmax_Ncharged",
              "EVT_ThrustEmin_Nneutral",
              "EVT_ThrustEmax_Nneutral"
              ]

#First stage BDT including event-level vars and vertex vars
#This is the default list used in the analysis
train_vars_vtx = [*train_vars, *[
                  "EVT_NtracksPV",
                  "EVT_NVertex",
                  "EVT_NKPi",
                  "EVT_ThrustEmin_NDV",
                  "EVT_ThrustEmax_NDV",
                  "EVT_dPV2DVmin",
                  "EVT_dPV2DVmax",
                  "EVT_dPV2DVave"
                  ]]

#Second stage training variables
train_vars_stage2 = ["EVT_CandMass",
                "EVT_CandN",
                "EVT_CandVtxFD",
                "EVT_CandVtxChi2",
                "EVT_CandPx",
                "EVT_CandPy",
                "EVT_CandPz",
                "EVT_CandP",
                "EVT_CandD0",
                "EVT_CandZ0",
                "EVT_CandAngleThrust",
                "EVT_DVd0_min",
                "EVT_DVd0_max",
                "EVT_DVd0_ave",
                "EVT_DVz0_min",
                "EVT_DVz0_max",
                "EVT_DVz0_ave",
                "EVT_PVmass",
                "EVT_Nominal_B_E"
               ]

fit_cut_vars = [ "EVT_MVA1",
                 "EVT_MVA2",
                 "EVT_ThrustDiff_E"
               ]

train_var_lists = { "train_vars" : train_vars,
                    "train_vars_vtx" : train_vars_vtx,
                    "train_vars_stage2" : train_vars_stage2,
                    "fit_cut_vars" : fit_cut_vars
                  }


#Decay modes used in first stage training and their respective file names
mode_names = {"Bd2KstNuNu": "p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu",
              "uds": "p8_ee_Zuds_ecm91",
              "cc": "p8_ee_Zcc_ecm91",
              "bb": "p8_ee_Zbb_ecm91"
              }

#Hemisphere energy difference cut, applied offline prior to MVA2 optimisation
energy_difference_cut = ">5"
mva1_min = 0.90
mva2_min = 0.90
mva1_max = 0.999
mva2_max = 0.999

# spline bins
mva1_spl_bins = 10
mva2_spl_bins = 20

# B production fractions
prod_frac = {"Bu": 0.43,
             "Bd": 0.43,
             "Bs": 0.096,
             "Lb": 0.037,
             "Bc": 0.0004
            }

prod_frac["Bd2KstNuNu"] = prod_frac["Bd"]
prod_frac["Bs2PhiNuNu"] = prod_frac["Bs"]

signal_bfs = {"Bd2KstNuNu": 1e-5,
              "Bs2PhiNuNu": 0.5e-5 # to include phi->KK
             }
