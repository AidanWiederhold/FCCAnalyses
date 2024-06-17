from config import train_var_lists

def run(input_files, vars_list):
    import uproot
    print("input_files: ", input_files)
    for inf in input_files:
        print(inf)
        output_file = inf.replace("/stage1", "/stage1_pickles").replace(".root", ".pkl")
        #df = uproot.concatenate(inf+":events", library="pd", how="zip", filter_name=vars_list )
        df = uproot.open(inf).get("events").pandas.df(vars_list)
        df.to_pickle(output_file)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', nargs="+", required=True, help='Select the input file(s).')
    #parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    parser.add_argument('--vars', type=str, required=True, help='Select the variables to keep, e.g "train_vars_vtx", "train_vars_stage2"')
    args = parser.parse_args()

    assert( args.vars in train_var_lists.keys() )

    run(args.input, vars_list=train_var_lists[args.vars][args.decay])

if __name__ == '__main__':
    main()