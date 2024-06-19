# stage1
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage1.py &> ${ANALYSISOUTPUT}logs/stage1.log
# pickle stage1
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ${ANALYSISOUTPUT}data/stage1/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --vars train_vars_vtx &> ${ANALYSISOUTPUT}logs/pickle_signal.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ${ANALYSISOUTPUT}data/stage1/p8_ee_Zbb_ecm91/* --vars train_vars_vtx &> ${ANALYSISOUTPUT}logs/pickle_bb_bkg.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ${ANALYSISOUTPUT}data/stage1/p8_ee_Zcc_ecm91/* --vars train_vars_vtx &> ${ANALYSISOUTPUT}logs/pickle_cc_bkg.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ${ANALYSISOUTPUT}data/stage1/p8_ee_Zss_ecm91/* --vars train_vars_vtx &> ${ANALYSISOUTPUT}logs/pickle_ss_bkg.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ${ANALYSISOUTPUT}data/stage1/p8_ee_Zud_ecm91/* --vars train_vars_vtx &> ${ANALYSISOUTPUT}logs/pickle_ud_bkg.log
# train bdt1
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/train_bdt1.py --vars vtx --signal_pkl ${ANALYSISOUTPUT}data/pickle/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb_pkl ${ANALYSISOUTPUT}data/pickle/p8_ee_Zbb_ecm91/* --cc_pkl ${ANALYSISOUTPUT}data/pickle/p8_ee_Zcc_ecm91/* --ss_pkl ${ANALYSISOUTPUT}data/pickle/p8_ee_Zss_ecm91/* --ud_pkl ${ANALYSISOUTPUT}data/pickle/p8_ee_Zud_ecm91/* --signal_root ${ANALYSISOUTPUT}data/stage1/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb_root ${ANALYSISOUTPUT}data/stage1/p8_ee_Zbb_ecm91/* --cc_root ${ANALYSISOUTPUT}data/stage1/p8_ee_Zcc_ecm91/* --ss_root ${ANALYSISOUTPUT}data/stage1/p8_ee_Zss_ecm91/* --ud_root ${ANALYSISOUTPUT}data/stage1/p8_ee_Zud_ecm91/* --output_root ${ANALYSISOUTPUT}data/bdt1/bdt1.root --output_joblib ${ANALYSISOUTPUT}data/bdt1/bdt1.joblib --roc_plot ${ANALYSISOUTPUT}plots/bdt1/roc.png --decay Bd2KstNuNu &> ${ANALYSISOUTPUT}logs/train_bdt1.log
# add bdt1 branch
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/add_bdt1.py &> ${ANALYSISOUTPUT}logs/add_bdt1.log
# plot bdt1
python ./examples/FCCee/flavour/b2snunu/scripts/bdt_plot.py --signal ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zbb_ecm91/* --cc ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zcc_ecm91/* --ss ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zss_ecm91/* --ud ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zud_ecm91/* --bdt1 ${ANALYSISOUTPUT}data/bdt1/bdt1.root --output ${ANALYSISOUTPUT}plots/bdt1/response.png --decay Bd2KstNuNu &> ${ANALYSISOUTPUT}logs/bdt1_plot.log
# bdt1 eff
python ./examples/FCCee/flavour/b2snunu/scripts/bdt_eff.py --signal ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zbb_ecm91/* --cc ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zcc_ecm91/* --ss ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zss_ecm91/* --ud ${ANALYSISOUTPUT}data/stage1_bdt/p8_ee_Zud_ecm91/* --bdt1 ${ANALYSISOUTPUT}data/bdt1/bdt1.root --output ${ANALYSISOUTPUT}plots/bdt1/eff.png --decay Bd2KstNuNu &> ${ANALYSISOUTPUT}logs/bdt1_eff.log
# loose cuts
# stage2
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage2.py &> ${ANALYSISOUTPUT}logs/stage2.log
# pickle stage2
# train bdt2
# add bdt2 branch
# plot bdt2
# bdt2 eff
# sensitivity
