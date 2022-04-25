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
"""
class analysis():
    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print (" init done, about to run")
    #__________________________________________________________
    def run(self, n_events, candidates):
        #df2 = (self.df.Range(100)
        df2 = (self.df)
                #.Define("EVT_MVA1", "EVT_MVA1"))
            
        #from config import stage1_branches
        branchList = ROOT.vector('string')()
        #branchList.push_back("EVT_MVA1")
        for branch in stage1_branches(candidates):
            branchList.push_back(branch)
        
        df2.Snapshot("events", self.outname, branchList)
"""

def main(input_file, output_file):
    inf = ROOT.TFile.Open(input_file, "READ")
    tree = inf.Get("events")
    outf = ROOT.TFile.Open(output_file, "RECREATE")
    out_tree = tree.CopyTree("")
    out_tree.Write()
    outf.Close()
    inf.Close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, required=True, help='Select the input file(s).')
    parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    parser.add_argument('--n_events', default = 0, type=int, help='Choose the number of events to process.')
    parser.add_argument('--n_cpus', default = 8, type=int, help='Choose the number of cpus to use.')
    parser.add_argument('--decay', required=True, type=str, help='Choose the decay to reconstruct.')
    args = parser.parse_args()

    main(args.input, args.output)

    """
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

    from config import decay_to_candidates, decay_to_pdgids, stage1_branches
    candidates = decay_to_candidates[args.decay]
    #child_pdgid, parent_pdgid = decay_to_pdgids[args.decay]
    import time
    start_time = time.time()
    analysis = analysis(input_files, args.output, n_cpus)
    analysis.run(n_events, candidates)

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
    """