import uproot
import pandas
import numpy as np
import argparse
import matplotlib.pyplot as plt
parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--bb',nargs="+", required=True, help='Select the input file(s).')
parser.add_argument('--cc',nargs="+", required=True, help='Select the input file(s).')
parser.add_argument('--ss',nargs="+", required=True, help='Select the input file(s).')
parser.add_argument('--ud',nargs="+", required=True, help='Select the input file(s).')
parser.add_argument('--signal',nargs="+", required=True, help='Select the input file(s).')
parser.add_argument('--output', type=str, required=True, help='Select the output file.')
#parser.add_argument('--decay', type=str, required=True, help='Select the reconstructed decay.')
args = parser.parse_args()

def load_df(input_files):
    mva_df = pandas.DataFrame()
    for input_name in input_files:
        with uproot.open(input_name) as inf:
            mva_df = pandas.concat([mva_df, inf["events"]["EVT_MVA1"].array(library="pd")])
    return mva_df

dfs = {"signal" : load_df(args.signal),
       "bbbar_df": load_df(args.inclusive_bbbar),
       "qqbar_df": load_df(args.inclusive_qqbar),
       "ccbar_df": load_df(args.inclusive_ccbar),
}

hist_setting = {
    "signal": {"hist_type": "bar", "colour": "orange"},
    "bbbar_df": {"hist_type": "step", "colour": "red"},
    "qqbar_df": {"hist_type": "step", "colour": "green"},
    "ccbar_df": {"hist_type": "step", "colour": "blue"},
}

plt.tight_layout()
mva_values = np.linspace(0., 1., 250)
#for _name, df in {"signal": dfs["bbbar_df"]}.items():
for name, df in dfs.items():
    eff_values = []
    initial_events = len(df)
    print(len(df))
    print(df)
    for mva_value in mva_values:
        df = df[df[0]>mva_value]
        eff = len(df)/initial_events
        eff_values.append(eff)
    plt.plot(mva_values, eff_values, color = hist_setting[name]["colour"], label=name)
plt.yscale('log')
plt.legend(loc="lower left")
plt.xlabel("BDT Response")
plt.ylabel("Efficiency")
plt.xlim(0., 1.)
plt.xticks([i/10. for i in range(0, 11)])
plt.grid(which="both")
plt.savefig(args.output, dpi=2000)
plt.savefig(args.output.replace("png", "pdf"))

# python ./scripts/mva_plot.py --inclusive_bbbar ./output/stage1/Bd2KstNuNu/p8_ee_Zbb_ecm91/inclusive/0.root --inclusive_ccbar ./output/stage1/Bd2KstNuNu/p8_ee_Zcc_ecm91/inclusive/119.root --inclusive_qqbar ./output/stage1/Bd2KstNuNu/p8_ee_Zuds_ecm91/inclsive/100.root --signal ./output/stage1/Bd2KstNuNu/p8_ee_Zbb_ecm91/signal/0.root --output ./Bd2KstNuNu_test_plot.png
# python ./scripts/mva_plot.py --inclusive_bbbar ./output/stage1/Bs2PhiNuNu/p8_ee_Zbb_ecm91/inclusive/100.root --inclusive_ccbar ./output/stage1/Bs2PhiNuNu/p8_ee_Zcc_ecm91/inclusive/10.root --inclusive_qqbar ./output/stage1/Bs2PhiNuNu/p8_ee_Zuds_ecm91/inclusive/0.root --signal ./output/stage1/Bs2PhiNuNu/p8_ee_Zbb_ecm91/signal/0.root --output ./Bs2PhiNuNu_test_plot.png