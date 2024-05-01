import sys
import ROOT
from array import array

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libawkward")
ROOT.gSystem.Load("libawkward-cpu-kernels")
ROOT.gSystem.Load("libFCCAnalyses")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"
        self.ncpu = ncpu

        if ncpu>1: # MT and self.df.Range() is not allowed but MT must be enabled before constructing a df
            ROOT.ROOT.EnableImplicitMT(ncpu) 
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print ("Input dataframe initialised!")
    #__________________________________________________________
    def run(self, n_events, decay, candidates, child_pdgid, parent_pdgid):
        print("Running...")

        if self.ncpu==1:
            df2 = self.df.Range(0, n_events)
        else:
            df2 = self.df
        
        df3 = (df2
               #############################################
               ##          Aliases for # in python        ##
               #############################################
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")


               #############################################
               ##MC record to study the Z->bb events types##
               #############################################               
               .Define("MC_PDG", "FCCAnalyses::MCParticle::get_pdg(Particle)")
               .Define("MC_n",   "int(MC_PDG.size())")
               .Define("MC_M1",  "FCCAnalyses::myUtils::getMC_parent(0,Particle,Particle0)")
               .Define("MC_M2",  "FCCAnalyses::myUtils::getMC_parent(1,Particle,Particle0)")
               .Define("MC_D1",  "FCCAnalyses::myUtils::getMC_daughter(0,Particle,Particle1)")
               .Define("MC_D2",  "FCCAnalyses::myUtils::getMC_daughter(1,Particle,Particle1)")
               .Define("MC_D3",  "FCCAnalyses::myUtils::getMC_daughter(2,Particle,Particle1)")
               .Define("MC_D4",  "FCCAnalyses::myUtils::getMC_daughter(3,Particle,Particle1)")
               .Define("MC_orivtx_x",   "FCCAnalyses::MCParticle::get_vertex_x(Particle)")
               .Define("MC_orivtx_y",   "FCCAnalyses::MCParticle::get_vertex_y(Particle)")
               .Define("MC_orivtx_z",   "FCCAnalyses::MCParticle::get_vertex_z(Particle)")
               .Define("MC_endvtx_x",   "FCCAnalyses::MCParticle::get_endPoint_x(Particle)")
               .Define("MC_endvtx_y",   "FCCAnalyses::MCParticle::get_endPoint_y(Particle)")
               .Define("MC_endvtx_z",   "FCCAnalyses::MCParticle::get_endPoint_z(Particle)")
               .Define("MC_p",   "FCCAnalyses::MCParticle::get_p(Particle)")
               .Define("MC_pt",  "FCCAnalyses::MCParticle::get_pt(Particle)")
               .Define("MC_px",  "FCCAnalyses::MCParticle::get_px(Particle)")
               .Define("MC_py",  "FCCAnalyses::MCParticle::get_py(Particle)")
               .Define("MC_pz",  "FCCAnalyses::MCParticle::get_pz(Particle)")
               .Define("MC_e",   "FCCAnalyses::MCParticle::get_e(Particle)")
               .Define("MC_m",   "FCCAnalyses::MCParticle::get_mass(Particle)")
               .Define("MC_q",   "FCCAnalyses::MCParticle::get_charge(Particle)")
               .Define("MC_eta", "FCCAnalyses::MCParticle::get_eta(Particle)")
               .Define("MC_phi", "FCCAnalyses::MCParticle::get_phi(Particle)")
               .Define("MC_TLV", "FCCAnalyses::MCParticle::get_tlv(Particle)")
               .Define("MC_q2", "FCCAnalyses::myUtils::children_q2(Particle, MC_D1, MC_D2, MC_D3, MC_D4)")
        )
        branchList = ROOT.vector('string')()
        desired_branches = [
                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2","MC_D3","MC_D4",
                "MC_p","MC_pt","MC_px","MC_py","MC_pz","MC_m", "MC_e","MC_eta","MC_phi", "MC_TLV", "MC_q2",
                ]
        for branchName in desired_branches:
            branchList.push_back(branchName)
        df3.Snapshot("events", self.outname, branchList)

if __name__ == "__main__":

    print("Initialising...")

    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    parser.add_argument('--n_events', default = 0, type=int, help='Choose the number of events to process.')
    parser.add_argument('--n_cpus', default = 8, type=int, help='Choose the number of cpus to use.')
    parser.add_argument('--decay', required=True, type=str, help='Choose the decay to reconstruct.')
    args = parser.parse_args()

    input_files = ROOT.vector('string')()
    if "*" in args.input:
        import glob
        file_list = glob.glob(args.input)
        for file_name in file_list:
            input_files.push_back(file_name)
    else:
        for inf in args.input:
            input_files.push_back(inf)
    n_events=args.n_events
    if n_events==0:
        for f in input_files:
            tf=ROOT.TFile.Open(str(f),"READ")
            tt=tf.Get("events")
            n_events+=tt.GetEntries()
        n_cpus=args.n_cpus
    else:
        print(f"WARNING: Cannot use multi-threading when running over a finite set of events. Setting n_cpus to 1.")
        n_cpus=1

    print("===============================STARTUP SUMMARY===============================")
    print(f"Input File(s)     : {args.input}")
    print(f"Output File       : {args.output}")
    print(f"Events to process : {n_events}")
    print(f"Number of CPUs    : {n_cpus}")
    print("=============================================================================")

    from config import decay_to_candidates, decay_to_pdgids, chi2_to_misid_rate
    candidates = decay_to_candidates[args.decay]
    child_pdgid, parent_pdgid = decay_to_pdgids[args.decay]
    import time
    start_time = time.time()
    analysis = analysis(input_files, args.output, n_cpus)
    analysis.run(n_events, args.decay, candidates, child_pdgid, parent_pdgid)

    elapsed_time = time.time() - start_time
    print  ("==============================COMPLETION SUMMARY=============================")
    print  ("Elapsed time (H:M:S)     :  ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ("Events Processed/Second  :  ",int(n_events/elapsed_time))
    print  ("Total Events Processed   :  ",int(n_events))
    print  ("=============================================================================")

    
    outf = ROOT.TFile( args.output, "update" )
    meta = ROOT.TTree( "metadata", "metadata informations" )
    n = array( "i", [ 0 ] )
    meta.Branch( "eventsProcessed", n, "eventsProcessed/I" )
    n[0]=n_events
    meta.Fill()
    p = ROOT.TParameter(int)( "eventsProcessed", n[0])
    p.Write()
    outf.Write()
    outf.Close()