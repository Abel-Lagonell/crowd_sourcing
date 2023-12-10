# sumo2nx.py
# Author: Quentin Goss

import os
import sys
import pantherine as purr
import math

def main():
    global OPTIONS; OPTIONS = get_options()
    
    # Nodes
    nod_xml = purr.mrf(OPTIONS.map_dir,r'*.nod.xml')
    nodes = purr.readXMLtag(nod_xml,'node')
    print("nodes: ", len(nodes))
    
    # Edges
    edg_xml = purr.mrf(OPTIONS.map_dir,r'*.edg.xml')
    edges = purr.readXMLtag(edg_xml,'edge')
    print("edges: ", len(edges))
    
    with open(OPTIONS.output,'w') as f:
        f.write("% from to weight id\n")
        
        # Each each is a connection
        n = 0; total = len(edges)
        for edge in edges:
            if edge['from'] == edge['to']:
                n += 1
                continue
                
            # Edges with shape
            try:
                length = length_from_shape(edge['shape'])
                
            # Edges w/o shape
            except KeyError:
                node_from = purr.filterdicts(nodes,'id',edge['from'])[0]
                node_to = purr.filterdicts(nodes,'id',edge['to'])[0]
                length = length_from_nodes(node_from,node_to)
                
            speed = float(edge['speed'])
            
            f.write("%s %s %.3f %s\n" % (edge['from'],edge['to'],length/speed, edge['id']))
                
            n+=1;purr.update(n,total,msg="Calculating edge lengths ")
            continue
        pass
    print()
    
    return
    
# Parse arguments from Command Line
def get_options():
    from optparse import OptionParser
    parser = OptionParser()
    #
    parser.add_option('--version', dest='version', action="store_true", default=False, help="Shows version information.")
    # Input
    parser.add_option('-m','--map.dir',dest='map_dir', type='string', default=None, help='Directory of sumo map.')
    parser.add_option('-o','--output',dest='output', type='string',default='map.nx', help='Output file. Reccomended to be .nx')
    #
    (options,args) = parser.parse_args()
    
    if options.version:
        version()
    elif options.map_dir == None:
        print("Please specify a SUMO map directory with -m.")
        sys.exit(0)
    return options
    
def version():
    print("~~ Sumo2nx Verison 1.0 by Quentin Goss~~")
    print("Converts simple SUMO files into a graph that may be")
    print(" used with networkx.")
    sys.exit(1)
    return
    
# Obtains the length of the edge given the shape string
# @param str shape_str = shape as a string
# @return float dist = length of shape
def length_from_shape(shape_str):
    shape_str = shape_str.split(' ')
    shape = []
    for xy_str in shape_str:
        x,y = xy_str.split(',')
        x = float(x); y = float(y)
        shape.append((x,y))
    dist = 0
    for i in range(1,len(shape)):
        x0,y0 = shape[i-1]
        x1,y1 = shape[i]
        dist += math.sqrt(math.pow(x0-x1,2)+math.pow(y0-y1,2))
    return dist


# Obtains the length of an edge given the start and end nodes
# @param dict node_from = Start
# @param dict node_to = End
# @return float dist = distance between the two nodes
def length_from_nodes(node_from,node_to):
    x0,y0 = (float(node_from['x']),float(node_from['y']))
    x1,y1 = (float(node_to['x']),float(node_to['y']))
    return math.sqrt(math.pow(x0-x1,2)+math.pow(y0-y1,2))
    
if __name__ == "__main__":
    main()
