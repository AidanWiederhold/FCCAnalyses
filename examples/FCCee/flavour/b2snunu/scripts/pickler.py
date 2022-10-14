def run(input_file, output_file, decay):
    import uproot
    from bdt_config import train_vars_vtx, loc
    inf = uproot.open(input_file)
    tree = inf['events']
    df = tree.arrays(library="pd", how="zip", filter_name=train_vars_vtx[decay])
    df.to_pickle(output_file)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Applies preselection cuts", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', nargs="+", required=True, help='Select the input file(s).')
    parser.add_argument('--output', type=str, required=True, help='Select the output file.')
    parser.add_argument('--decay', type=str, required=True, help='Select the decay.')
    args = parser.parse_args()

    run(args.input, args.output, args.decay)

if __name__ == '__main__':
    main()
