# stage1
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage1.py &> ./outputs/logs/stage1.log
# pickle stage1
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ./outputs/data/stage1/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --vars train_vars_vtx &> ./outputs/logs/pickle_signal.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ./outputs/data/stage1/p8_ee_Zbb_ecm91/* --vars train_vars_vtx &> ./outputs/logs/pickle_bb_bkg.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ./outputs/data/stage1/p8_ee_Zcc_ecm91/* --vars train_vars_vtx &> ./outputs/logs/pickle_cc_bkg.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ./outputs/data/stage1/p8_ee_Zss_ecm91/* --vars train_vars_vtx &> ./outputs/logs/pickle_ss_bkg.log
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ./outputs/data/stage1/p8_ee_Zud_ecm91/* --vars train_vars_vtx &> ./outputs/logs/pickle_ud_bkg.log
# train bdt1
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/train_bdt1.py --vars vtx --signal_pkl ./outputs/data/pickle/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb_pkl ./outputs/data/pickle/p8_ee_Zbb_ecm91/* --cc_pkl ./outputs/data/pickle/p8_ee_Zcc_ecm91/* --ss_pkl ./outputs/data/pickle/p8_ee_Zss_ecm91/* --ud_pkl ./outputs/data/pickle/p8_ee_Zud_ecm91/* --signal_root ./outputs/data/stage1/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb_root ./outputs/data/stage1/p8_ee_Zbb_ecm91/* --cc_root ./outputs/data/stage1/p8_ee_Zcc_ecm91/* --ss_root ./outputs/data/stage1/p8_ee_Zss_ecm91/* --ud_root ./outputs/data/stage1/p8_ee_Zud_ecm91/* --output_root ./outputs/data/bdt1/bdt1.root --output_joblib ./outputs/data/bdt1/bdt1.joblib --roc_plot ./outputs/plots/bdt1/roc.png --decay Bd2KstNuNu &> ./outputs/logs/train_bdt1.log
# add bdt1 branch
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/add_bdt1.py &> ./outputs/logs/add_bdt1.log
# plot bdt1
python ./examples/FCCee/flavour/b2snunu/scripts/bdt_plot.py --signal ./outputs/data/stage1_bdt/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb ./outputs/data/stage1_bdt/p8_ee_Zbb_ecm91/* --cc ./outputs/data/stage1_bdt/p8_ee_Zcc_ecm91/* --ss ./outputs/data/stage1_bdt/p8_ee_Zss_ecm91/* --ud ./outputs/data/stage1_bdt/p8_ee_Zud_ecm91/* --bdt1 ./outputs/data/bdt1/bdt1.root --output ./outputs/plots/bdt1/response.png --decay Bd2KstNuNu &> ./outputs/logs/bdt1_plot.log
# bdt1 eff
python ./examples/FCCee/flavour/b2snunu/scripts/bdt_eff.py --signal ./outputs/data/stage1_bdt/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu/* --bb ./outputs/data/stage1_bdt/p8_ee_Zbb_ecm91/* --cc ./outputs/data/stage1_bdt/p8_ee_Zcc_ecm91/* --ss ./outputs/data/stage1_bdt/p8_ee_Zss_ecm91/* --ud ./outputs/data/stage1_bdt/p8_ee_Zud_ecm91/* --bdt1 ./outputs/data/bdt1/bdt1.root --output ./outputs/plots/bdt1/eff.png --decay Bd2KstNuNu &> ./outputs/logs/bdt1_eff.log
# loose cuts
# stage2
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage2.py &> ./outputs/logs/stage2.log
# pickle stage2
# train bdt2
# add bdt2 branch
# plot bdt2
# bdt2 eff
# sensitivity
