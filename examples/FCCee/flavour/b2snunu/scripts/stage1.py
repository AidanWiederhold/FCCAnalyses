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

#TODO change this to args.decay instead of Bd2KstNuNu
ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt("Bd2KstNuNu_BDT", "root://eospublic.cern.ch//eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2KstNuNu/xgb_bdt_vtx.root");
computeModel = TMVA::Experimental::Compute<18, float>(bdt);
''')

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
    def run(self, n_events, MVA_cut, decay, candidates, child_pdgid, parent_pdgid):
        print("Running...")
        MVAFilter=f"EVT_MVA1>{MVA_cut}"

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
               .Define("MC_PDG", "MCParticle::get_pdg(Particle)")
               .Define("MC_n",   "int(MC_PDG.size())")
               #.Define("MC_M1",  "myUtils::get_MCMother1(Particle,Particle0)")
               #.Define("MC_M2",  "myUtils::get_MCMother2(Particle,Particle0)")
               #.Define("MC_D1",  "myUtils::get_MCDaughter1(Particle,Particle1)")
               #.Define("MC_D2",  "myUtils::get_MCDaughter2(Particle,Particle1)")
               .Define("MC_M1",  "myUtils::getMC_parent(0,Particle,Particle0)")
               .Define("MC_M2",  "myUtils::getMC_parent(1,Particle,Particle0)")
               .Define("MC_D1",  "myUtils::getMC_daughter(0,Particle,Particle1)")
               .Define("MC_D2",  "myUtils::getMC_daughter(1,Particle,Particle1)")
               .Define("MC_D3",  "myUtils::getMC_daughter(2,Particle,Particle1)")
               .Define("MC_D4",  "myUtils::getMC_daughter(3,Particle,Particle1)")
               .Define("MC_orivtx_x",   "MCParticle::get_vertex_x(Particle)")
               .Define("MC_orivtx_y",   "MCParticle::get_vertex_y(Particle)")
               .Define("MC_orivtx_z",   "MCParticle::get_vertex_z(Particle)")
               .Define("MC_endvtx_x",   "MCParticle::get_endPoint_x(Particle)")
               .Define("MC_endvtx_y",   "MCParticle::get_endPoint_y(Particle)")
               .Define("MC_endvtx_z",   "MCParticle::get_endPoint_z(Particle)")
               .Define("MC_p",   "MCParticle::get_p(Particle)")
               .Define("MC_pt",  "MCParticle::get_pt(Particle)")
               .Define("MC_px",  "MCParticle::get_pt(Particle)")
               .Define("MC_py",  "MCParticle::get_pt(Particle)")
               .Define("MC_pz",  "MCParticle::get_pt(Particle)")
               .Define("MC_e",   "MCParticle::get_e(Particle)")
               .Define("MC_m",   "MCParticle::get_mass(Particle)")
               .Define("MC_q",   "MCParticle::get_charge(Particle)")
               .Define("MC_eta", "MCParticle::get_eta(Particle)")
               .Define("MC_phi", "MCParticle::get_phi(Particle)")
               

               #############################################
               ##               Build MC Vertex           ##
               #############################################
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
               .Define("MC_Vertex_x",    "myUtils::get_MCVertex_x(MCVertexObject)")
               .Define("MC_Vertex_y",    "myUtils::get_MCVertex_y(MCVertexObject)")
               .Define("MC_Vertex_z",    "myUtils::get_MCVertex_z(MCVertexObject)")
               .Define("MC_Vertex_ind",  "myUtils::get_MCindMCVertex(MCVertexObject)")
               .Define("MC_Vertex_ntrk", "myUtils::get_NTracksMCVertex(MCVertexObject)")
               .Define("MC_Vertex_n",    "int(MC_Vertex_x.size())")
               .Define("MC_Vertex_PDG",  "myUtils::get_MCpdgMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGmother",  "myUtils::get_MCpdgMotherMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGgmother", "myUtils::get_MCpdgGMotherMCVertex(MCVertexObject, Particle)")


               #############################################
               ##              Build Reco Vertex          ##
               #############################################
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")


               #############################################
               ##          Build PV var and filter        ##
               #############################################
               .Define("EVT_hasPV",    "myUtils::hasPV(VertexObject)")
               .Define("EVT_NtracksPV", "float(myUtils::get_PV_ntracks(VertexObject))")
               .Define("EVT_NVertex",   "float(VertexObject.size())")
               .Filter("EVT_hasPV==1")


               #############################################
               ##          Build RECO P with PID          ##
               #############################################
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")
               

               #############################################
               ##    Build RECO P with PID at vertex      ##
               #############################################
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")


               #############################################
               ##         Build vertex variables          ##
               #############################################
               .Define("Vertex_x",        "myUtils::get_Vertex_x(VertexObject)")
               .Define("Vertex_y",        "myUtils::get_Vertex_y(VertexObject)")
               .Define("Vertex_z",        "myUtils::get_Vertex_z(VertexObject)")
               .Define("Vertex_xErr",     "myUtils::get_Vertex_xErr(VertexObject)")
               .Define("Vertex_yErr",     "myUtils::get_Vertex_yErr(VertexObject)")
               .Define("Vertex_zErr",     "myUtils::get_Vertex_zErr(VertexObject)")

               .Define("Vertex_chi2",     "myUtils::get_Vertex_chi2(VertexObject)")
               .Define("Vertex_mcind",    "myUtils::get_Vertex_indMC(VertexObject)")
               .Define("Vertex_ind",      "myUtils::get_Vertex_ind(VertexObject)")
               .Define("Vertex_isPV",     "myUtils::get_Vertex_isPV(VertexObject)")
               .Define("Vertex_ntrk",     "myUtils::get_Vertex_ntracks(VertexObject)")
               .Define("Vertex_n",        "int(Vertex_x.size())")
               .Define("Vertex_mass",     "myUtils::get_Vertex_mass(VertexObject,RecoPartPIDAtVertex)")

               .Define("Vertex_d2PV",     "myUtils::get_Vertex_d2PV(VertexObject,-1)")
               .Define("Vertex_d2PVx",    "myUtils::get_Vertex_d2PV(VertexObject,0)")
               .Define("Vertex_d2PVy",    "myUtils::get_Vertex_d2PV(VertexObject,1)")
               .Define("Vertex_d2PVz",    "myUtils::get_Vertex_d2PV(VertexObject,2)")
               
               .Define("Vertex_d2PVErr",  "myUtils::get_Vertex_d2PVError(VertexObject,-1)")
               .Define("Vertex_d2PVxErr", "myUtils::get_Vertex_d2PVError(VertexObject,0)")
               .Define("Vertex_d2PVyErr", "myUtils::get_Vertex_d2PVError(VertexObject,1)")
               .Define("Vertex_d2PVzErr", "myUtils::get_Vertex_d2PVError(VertexObject,2)")
               
               .Define("Vertex_d2PVSig",  "Vertex_d2PV/Vertex_d2PVErr")
               .Define("Vertex_d2PVxSig", "Vertex_d2PVx/Vertex_d2PVxErr")
               .Define("Vertex_d2PVySig", "Vertex_d2PVy/Vertex_d2PVyErr")
               .Define("Vertex_d2PVzSig", "Vertex_d2PVz/Vertex_d2PVzErr")

               .Define("Vertex_d2MC",     "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,-1)")
               .Define("Vertex_d2MCx",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,0)")
               .Define("Vertex_d2MCy",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,1)")
               .Define("Vertex_d2MCz",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,2)")

               .Define("EVT_dPV2DVmin",   "myUtils::get_dPV2DV_min(Vertex_d2PV)")
               .Define("EVT_dPV2DVmax",   "myUtils::get_dPV2DV_max(Vertex_d2PV)")
               .Define("EVT_dPV2DVave",   "myUtils::get_dPV2DV_ave(Vertex_d2PV)")
               

               #############################################
               ##        Build Kstz -> KPi  candidates      ##
               #############################################
               .Define(f"{candidates}Candidates",         f"myUtils::build_{decay}(VertexObject,RecoPartPIDAtVertex)")


               #############################################
               ##       Filter Kstz -> KPi candidates      ##
               ############################################# 
               .Define(f"EVT_N{candidates}",              f"float(myUtils::getFCCAnalysesComposite_N({candidates}Candidates))")
               .Filter(f"EVT_N{candidates}>0")


               #############################################
               ##    Attempt to add a truth match         ##
               #############################################
               #.Define("TruthMatching" ,f"myUtils::add_truthmatched2({candidates}Candidates, MCParticles, MCRecoAssociations0, ReconstructedParticles, MCRecoAssociations1)")
               .Define("TruthMatching" ,f"myUtils::add_truthmatched2({candidates}Candidates, Particle, VertexObject, MCRecoAssociations0, ReconstructedParticles, MCRecoAssociations1)")


               #############################################
               ##              Build the thrust           ##
               ############################################# 
               .Define("RP_e",          "ReconstructedParticle::get_e(RecoPartPIDAtVertex)")
               .Define("RP_px",         "ReconstructedParticle::get_px(RecoPartPIDAtVertex)")
               .Define("RP_py",         "ReconstructedParticle::get_py(RecoPartPIDAtVertex)")
               .Define("RP_pz",         "ReconstructedParticle::get_pz(RecoPartPIDAtVertex)")
               .Define("RP_charge",     "ReconstructedParticle::get_charge(RecoPartPIDAtVertex)")
              
               .Define("EVT_thrustNP",      'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define("RP_thrustangleNP",  'Algorithms::getAxisCosTheta(EVT_thrustNP, RP_px, RP_py, RP_pz)')
               .Define("EVT_thrust",        'Algorithms::getThrustPointing(RP_thrustangleNP, RP_e, EVT_thrustNP, 1.)')
               .Define("RP_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')

               
               #############################################
               ##        Get thrust related values        ##
               ############################################# 
               ##hemis0 == negative angle == max energy hemisphere if pointing
               ##hemis1 == positive angle == min energy hemisphere if pointing
               .Define("EVT_thrusthemis0_n",    "Algorithms::getAxisN(0)(RP_thrustangle, RP_charge)")
               .Define("EVT_thrusthemis1_n",    "Algorithms::getAxisN(1)(RP_thrustangle, RP_charge)")
               .Define("EVT_thrusthemis0_e",    "Algorithms::getAxisEnergy(0)(RP_thrustangle, RP_charge, RP_e)")
               .Define("EVT_thrusthemis1_e",    "Algorithms::getAxisEnergy(1)(RP_thrustangle, RP_charge, RP_e)")

               .Define("EVT_ThrustEmax_E",         "EVT_thrusthemis0_e.at(0)")
               .Define("EVT_ThrustEmax_Echarged",  "EVT_thrusthemis0_e.at(1)")
               .Define("EVT_ThrustEmax_Eneutral",  "EVT_thrusthemis0_e.at(2)")
               .Define("EVT_ThrustEmax_N",         "float(EVT_thrusthemis0_n.at(0))")
               .Define("EVT_ThrustEmax_Ncharged",  "float(EVT_thrusthemis0_n.at(1))")
               .Define("EVT_ThrustEmax_Nneutral",  "float(EVT_thrusthemis0_n.at(2))")

               .Define("EVT_ThrustEmin_E",         "EVT_thrusthemis1_e.at(0)")
               .Define("EVT_ThrustEmin_Echarged",  "EVT_thrusthemis1_e.at(1)")
               .Define("EVT_ThrustEmin_Eneutral",  "EVT_thrusthemis1_e.at(2)")
               .Define("EVT_ThrustEmin_N",         "float(EVT_thrusthemis1_n.at(0))")
               .Define("EVT_ThrustEmin_Ncharged",  "float(EVT_thrusthemis1_n.at(1))")
               .Define("EVT_ThrustEmin_Nneutral",  "float(EVT_thrusthemis1_n.at(2))")


               .Define("Vertex_thrust_angle",   "myUtils::get_Vertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               .Define("DVertex_thrust_angle",  "myUtils::get_DVertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               ###0 == negative angle==max energy , 1 == positive angle == min energy
               .Define("Vertex_thrusthemis_emin",    "myUtils::get_Vertex_thrusthemis(Vertex_thrust_angle, 1)")
               .Define("Vertex_thrusthemis_emax",    "myUtils::get_Vertex_thrusthemis(Vertex_thrust_angle, 0)")

               .Define("EVT_ThrustEmin_NDV", "float(myUtils::get_Npos(DVertex_thrust_angle))")
               .Define("EVT_ThrustEmax_NDV", "float(myUtils::get_Nneg(DVertex_thrust_angle))")

               .Define("EVT_Thrust_Mag",  "EVT_thrust.at(0)")
               .Define("EVT_Thrust_X",    "EVT_thrust.at(1)")
               .Define("EVT_Thrust_XErr", "EVT_thrust.at(2)")
               .Define("EVT_Thrust_Y",    "EVT_thrust.at(3)")
               .Define("EVT_Thrust_YErr", "EVT_thrust.at(4)")
               .Define("EVT_Thrust_Z",    "EVT_thrust.at(5)")
               .Define("EVT_Thrust_ZErr", "EVT_thrust.at(6)")


               .Define("DV_tracks", "myUtils::get_pseudotrack(VertexObject,RecoPartPIDAtVertex)")

               .Define("DV_d0",            "myUtils::get_trackd0(DV_tracks)")
               .Define("DV_z0",            "myUtils::get_trackz0(DV_tracks)")

               # Build MVA 
               .Define("MVAVec", ROOT.computeModel, ("EVT_ThrustEmin_E",        "EVT_ThrustEmax_E",
                                                     "EVT_ThrustEmin_Echarged", "EVT_ThrustEmax_Echarged",
                                                     "EVT_ThrustEmin_Eneutral", "EVT_ThrustEmax_Eneutral",
                                                     "EVT_ThrustEmin_Ncharged", "EVT_ThrustEmax_Ncharged",
                                                     "EVT_ThrustEmin_Nneutral", "EVT_ThrustEmax_Nneutral",
                                                     "EVT_NtracksPV",           "EVT_NVertex",
                                                     f"EVT_N{candidates}",                "EVT_ThrustEmin_NDV",
                                                     "EVT_ThrustEmax_NDV",      "EVT_dPV2DVmin",
                                                     "EVT_dPV2DVmax",           "EVT_dPV2DVave"))
               .Define("EVT_MVA1", "MVAVec.at(0)")
               .Filter(MVAFilter) 

               .Define(f"{candidates}Candidates_mass",    f"myUtils::getFCCAnalysesComposite_mass({candidates}Candidates)")
               .Define(f"{candidates}Candidates_q",       f"myUtils::getFCCAnalysesComposite_charge({candidates}Candidates)")
               .Define(f"{candidates}Candidates_vertex",  f"myUtils::getFCCAnalysesComposite_vertex({candidates}Candidates)")
               .Define(f"{candidates}Candidates_mcvertex",f"myUtils::getFCCAnalysesComposite_mcvertex({candidates}Candidates,VertexObject)")
               .Define(f"{candidates}Candidates_truth",   f"myUtils::getFCCAnalysesComposite_truthMatch({candidates}Candidates)")
               .Define(f"{candidates}Candidates_px",      f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates,0)")
               .Define(f"{candidates}Candidates_py",      f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates,1)")
               .Define(f"{candidates}Candidates_pz",      f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates,2)")
               .Define(f"{candidates}Candidates_p",       f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates,-1)")
               .Define(f"{candidates}Candidates_B",       f"myUtils::getFCCAnalysesComposite_B({candidates}Candidates, VertexObject, RecoPartPIDAtVertex)")
               
               .Define(f"{candidates}Candidates_track",   f"myUtils::getFCCAnalysesComposite_track({candidates}Candidates, VertexObject)")
               .Define(f"{candidates}Candidates_d0",      f"myUtils::get_trackd0({candidates}Candidates_track)")
               .Define(f"{candidates}Candidates_z0",      f"myUtils::get_trackz0({candidates}Candidates_track)")

               .Define(f"{candidates}Candidates_anglethrust", f"myUtils::getFCCAnalysesComposite_anglethrust({candidates}Candidates, EVT_thrust)")
               .Define("CUT_hasCandEmin",           f"myUtils::has_anglethrust_emin({candidates}Candidates_anglethrust)")
               .Filter("CUT_hasCandEmin>0")
               
               .Define(f"{candidates}Candidates_h1px",   f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0, 0)")
               .Define(f"{candidates}Candidates_h1py",   f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0, 1)")
               .Define(f"{candidates}Candidates_h1pz",   f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0, 2)")
               .Define(f"{candidates}Candidates_h1p",    f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0, -1)")
               .Define(f"{candidates}Candidates_h1q",    f"myUtils::getFCCAnalysesComposite_q({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define(f"{candidates}Candidates_h1m",    f"myUtils::getFCCAnalysesComposite_mass({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define(f"{candidates}Candidates_h1type", f"myUtils::getFCCAnalysesComposite_type({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define(f"{candidates}Candidates_h1d0",   f"myUtils::getFCCAnalysesComposite_d0({candidates}Candidates, VertexObject, 0)")
               .Define(f"{candidates}Candidates_h1z0",   f"myUtils::getFCCAnalysesComposite_z0({candidates}Candidates, VertexObject, 0)")
               
               .Define(f"{candidates}Candidates_h2px",   f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1, 0)")
               .Define(f"{candidates}Candidates_h2py",   f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1, 1)")
               .Define(f"{candidates}Candidates_h2pz",   f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1, 2)")
               .Define(f"{candidates}Candidates_h2p",    f"myUtils::getFCCAnalysesComposite_p({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1, -1)")
               .Define(f"{candidates}Candidates_h2q",    f"myUtils::getFCCAnalysesComposite_q({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define(f"{candidates}Candidates_h2m",    f"myUtils::getFCCAnalysesComposite_mass({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define(f"{candidates}Candidates_h2type", f"myUtils::getFCCAnalysesComposite_type({candidates}Candidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define(f"{candidates}Candidates_h2d0",   f"myUtils::getFCCAnalysesComposite_d0({candidates}Candidates, VertexObject, 1)")
               .Define(f"{candidates}Candidates_h2z0",   f"myUtils::getFCCAnalysesComposite_z0({candidates}Candidates, VertexObject, 1)")
               
               .Define(f"True{candidates}_vertex",        f"myUtils::get_trueVertex(MCVertexObject,Particle,Particle0, {child_pdgid}, {parent_pdgid})")
               .Define(f"True{candidates}_track",         f"myUtils::get_truetrack(True{candidates}_vertex, MCVertexObject, Particle)")
               .Define(f"True{candidates}_d0",            f"myUtils::get_trackd0(True{candidates}_track)")
               .Define(f"True{candidates}_z0",            f"myUtils::get_trackz0(True{candidates}_track)")
           )
        
        branchList = ROOT.vector('string')()
        for branchName in [
                
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
                
                "EVT_MVA1",
                ]:
            branchList.push_back(branchName)
        df3.Snapshot("events", self.outname, branchList)

if __name__ == "__main__":

    print("Initialising...")

    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input',nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    parser.add_argument('--MVA_cut', default = -1., type=float, help='Choose the MVA cut.')
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
    print(f"MVA Cut           : {args.MVA_cut}")
    print(f"Number of CPUs    : {n_cpus}")
    print("=============================================================================")

    from config import decay_to_candidates, decay_to_pdgids
    candidates = decay_to_candidates[args.decay]
    child_pdgid, parent_pdgid = decay_to_pdgids[args.decay]
    import time
    start_time = time.time()
    analysis = analysis(input_files, args.output, n_cpus)
    analysis.run(n_events, args.MVA_cut, args.decay, candidates, child_pdgid, parent_pdgid)

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