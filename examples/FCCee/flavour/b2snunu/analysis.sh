# stage1
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage1.py &> ./outputs/logs/stage1.log
# pickle stage1
python ./examples/FCCee/flavour/b2snunu/scripts/pickler.py --input ./outputs/data/stage1/p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu.root --vars train_vars_vtx &> ./outputs/logs/pickler.log
# train bdt1
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/train_bdt1.py &> ./outputs/logs/train_bdt1.log
# add bdt1 branch
# plot bdt1
# bdt1 eff
# loose cuts
# stage2
fccanalysis run examples/FCCee/flavour/b2snunu/scripts/stage2.py &> ./outputs/logs/stage2.log
# pickle stage2
# train bdt2
# add bdt2 branch
# plot bdt2
# bdt2 eff
# sensitivity
