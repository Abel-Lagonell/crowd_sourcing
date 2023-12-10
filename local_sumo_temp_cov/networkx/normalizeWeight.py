# normalizeWeight.py
# Normalizes the weight of a nx graph
import sys

def main():
    options = get_options()
    weights = []
    with open(options.nx,'r') as f:
        for line in f:
            if '%' in line:
                continue
            weights.append(float(line.split(' ')[2]))
            continue
        pass
    min_weight = min(weights)
    max_weight = max(weights)
    with open("norm.nx",'w') as norm_nx:
        with open(options.nx,'r') as f:
            for line in f:
                if '%' in line:
                    norm_nx.write(line)
                    continue
                line = line.split(' ')
                weight = (float(line[2]) - min_weight)/(max_weight - min_weight)
                line[2] = str(weight)
                norm_nx.write(line[0])
                for i,item in enumerate(line[1:],1):
                    norm_nx.write(' %s' % (line[i]))
                continue
            pass
        pass
    return

# Parse arguments from Command Line
def get_options():
    from optparse import OptionParser
    parser = OptionParser()
    #
    parser.add_option('-i','--nx', dest='nx', default=None, help=".nx graph file")
    #
    (options,args) = parser.parse_args()
    
    if options.nx == None:
        print("Please specify a .nx graph with --nx.")
        sys.exit(0)
    return options

if __name__ == "__main__":
    main()
