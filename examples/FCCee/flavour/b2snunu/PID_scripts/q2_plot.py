import uproot
import matplotlib.pyplot as plt
import ROOT as r
import config as cfg

args_decay = "Bd2KstNuNu"
candidate_PDGID, B_PDGID = cfg.decay_to_pdgids[args_decay]
B_PDGID = int(B_PDGID)
candidate_PDGID = int(candidate_PDGID)
nu_PDGIDs = [12,14,16]

def map_d_id(event, d_index):
    if d_index!=-999:
        return int(event.MC_PDG[d_index])
    else:
        return -999

def d_ids_to_q2_index(d1, d2):
    if d1>d2:
        _ = d2
        d2 = d1
        d1 = d2
    if d1==1:
        if d2==2:
            return 0
        if d2==3:
            return 1
    if d1==2:
        return 2

q2_vals = []
m_vals = []

files= ["./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/14.root", "./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/44.root", "./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/32.root", "./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/45.root", "./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/33.root", "./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/49.root", "./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/40.root"]
tree = r.TChain("events")
for file_name in files:
    tree.Add(file_name)
for i, event in enumerate(tree):
    for particle_index, PDGID in enumerate(event.MC_PDG):
        d_ids_map = {}
        d_indexes_map = {}
        d_ids = []
        if abs(int(PDGID))==999:
            mother_index = event.MC_M1[particle_index]
            gmother_index = event.MC_M1[event.MC_M1[particle_index]]
            if mother_index!=-999:
                mother_id = event.MC_PDG[mother_index]
            else:
                mother_id = -999
            if gmother_index!=-999:
                gmother_id = event.MC_PDG[gmother_index]
            else:
                gmother_index = -999
            print("yo", gmother_id, mother_id, PDGID)
            print(map_d_id(event,event.MC_D1[particle_index]), map_d_id(event,event.MC_D2[particle_index]), map_d_id(event,event.MC_D3[particle_index]), map_d_id(event,event.MC_D4[particle_index]))
        if abs(int(PDGID)) == B_PDGID:
            d_ids_map[map_d_id(event, event.MC_D1[particle_index])] = 1
            d_ids_map[map_d_id(event, event.MC_D2[particle_index])] = 2
            d_ids_map[map_d_id(event, event.MC_D3[particle_index])] = 3
            d_ids_map[map_d_id(event, event.MC_D4[particle_index])] = 4
            d_indexes_map[map_d_id(event, event.MC_D1[particle_index])] = event.MC_D1[particle_index]
            d_indexes_map[map_d_id(event, event.MC_D2[particle_index])] = event.MC_D2[particle_index]
            d_indexes_map[map_d_id(event, event.MC_D3[particle_index])] = event.MC_D3[particle_index]
            d_indexes_map[map_d_id(event, event.MC_D4[particle_index])] = event.MC_D4[particle_index]
            d_ids = [id_ for id_ in d_ids_map.keys() if id_!=-999]
            #print(d_ids)
            #if 511 in d_ids or -511 in d_ids:
            #print(d_ids)
            #if ((321 in d_ids and -211 in d_ids) or (-321 in d_ids and 211 in d_ids)) and not 22 in d_ids:
            #    print(d_ids)
            if len(d_ids)==3:
                #print(d_ids)
                """
                if (321 in d_ids and -211 in d_ids) and 22 in d_ids:
                    #print(d_ids)
                    #print(d_indexes_map[22], map_d_id(event, event.MC_D1[d_indexes_map[22]]), map_d_id(event, event.MC_D2[d_indexes_map[22]]), map_d_id(event, event.MC_D3[d_indexes_map[22]]), map_d_id(event, event.MC_D4[d_indexes_map[22]]))
                    #q2_vals.append(event.MC_q2[d_indexes_map[22]])
                    K_vector = r.TLorentzVector(event.MC_px[d_indexes_map[321]], event.MC_py[d_indexes_map[321]], event.MC_pz[d_indexes_map[321]], event.MC_e[d_indexes_map[321]])
                    pi_vector = r.TLorentzVector(event.MC_px[d_indexes_map[-211]], event.MC_py[d_indexes_map[-211]], event.MC_pz[d_indexes_map[-211]], event.MC_e[d_indexes_map[-211]])
                    B_vector = r.TLorentzVector(event.MC_px[event.MC_M1[particle_index]], event.MC_py[event.MC_M1[particle_index]], event.MC_pz[event.MC_M1[particle_index]], event.MC_e[event.MC_M1[particle_index]])
                    m_vals.append(B_vector.M())
                    q2_vals.append((B_vector-(K_vector+pi_vector)).M2())
                if (-321 in d_ids and 211 in d_ids) and 22 in d_ids:
                    #print(d_ids)
                    #print(d_indexes_map[22], map_d_id(event, event.MC_D1[d_indexes_map[22]]), map_d_id(event, event.MC_D2[d_indexes_map[22]]), map_d_id(event, event.MC_D3[d_indexes_map[22]]), map_d_id(event, event.MC_D4[d_indexes_map[22]]))
                    #q2_vals.append(event.MC_q2[d_indexes_map[22]])
                    K_vector = r.TLorentzVector(event.MC_px[d_indexes_map[-321]], event.MC_py[d_indexes_map[-321]], event.MC_pz[d_indexes_map[-321]], event.MC_e[d_indexes_map[-321]])
                    pi_vector = r.TLorentzVector(event.MC_px[d_indexes_map[211]], event.MC_py[d_indexes_map[211]], event.MC_pz[d_indexes_map[211]], event.MC_e[d_indexes_map[211]])
                    B_vector = r.TLorentzVector(event.MC_px[event.MC_M1[particle_index]], event.MC_py[event.MC_M1[particle_index]], event.MC_pz[event.MC_M1[particle_index]], event.MC_e[event.MC_M1[particle_index]])
                    m_vals.append(B_vector.M())
                    q2_vals.append((B_vector-(K_vector+pi_vector)).M2())
                """
                if candidate_PDGID in d_ids:
                    for nu in nu_PDGIDs:
                        if (nu in d_ids and -nu in d_ids):
                            #print("yay", nu)
                            #print(event.MC_q2[particle_index])
                            q2_vals.append(event.MC_q2[particle_index][d_ids_to_q2_index(d_ids_map[nu], d_ids_map[-nu])])
    #if i>100:
    #    break




#plt.hist(m_vals, 100)
#plt.savefig("m_plot.png", dpi=1000)
#plt.clf()
plt.hist(q2_vals, 100)
plt.savefig("q2_plot.png", dpi=1000)
"""
input_files = ["./output_new_var/root/stage0/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/14.root:events"] 

branches = ["MC_PDG", "MC_D1", "MC_D2", "MC_D3", "MC_D4", "MC_q2"]

for arr in uproot.iterate(input_files, expressions=branches, step_size=100, library="np"):
    n_events = len(arr)
    print(arr)
    print(arr["MC_PDG"])
    for event_index, event in enumerate(arr["MC_PDG"]):
        if event_index<n_events:
            #print(f"{100*event_index/n_events:.2f} % of events determined", end="\r")
            for particle_index, PDGID in enumerate(event):
                #candidate_mass = arr[f"{candidate}Candidates_mass"][event_index][candidate_number]
                print(n_events, event_index, event, len(event), particle_index, PDGID)
"""