# nxasp.py
# Author: Quentin Goss
# "NetworkX All Shortest Paths" proprocess' a networkx graph to
#  to find every combination of shortest path.

import os
import sys
import pantherine as purr
import networkx as nx
import numpy

def main():
    banner()
    global OPTIONS; OPTIONS = get_options()
    global SN; SN = read_graph()
    
    nids = list(SN.nodes)[:10]

    weights = []
    n = 0; total = 100*100#len(nids)*len(nids)
    for i,nid_from in enumerate(nids):
        row = list()
        for j,nid_to in enumerate(nids):
            try:
                path = nx.dijkstra_path(SN,nid_from,nid_to)
                weight = path_info(SN,path)
                if weight == 0:
                    weight = float("inf")
            except nx.NetworkXNoPath:
                weight = float("inf")
            row.append(weight)
            n += 1
            if n % 10 == 0:
                print("Progress %d/%d %.2f%%" % (n,total, n/total*100), end='\r')
            continue
        weights.append(tuple(row))
        continue
    weights = tuple(weights)
    
    
    print('%10s ' % (''),end='')
    for i,row in enumerate(weights):
        print('%7s ' % (nids[i][:7]), end='')
    print()
    for i,row in enumerate(weights):
        print('%10s:' % (nids[i][:10]), end='')
        for val in row:
            if val == float('inf'):                
                print('    inf ',end='')
            else:
                print('%7.2f ' % (val),end='')
        print()
    purr.save('weight.pydata',weights)
    return

# Parse arguments from Command Line
def get_options():
    from optparse import OptionParser
    parser = OptionParser()
    # Input
    parser.add_option('-i','--nx',dest='nx', type='string', help='NetworkX graph with weight and EIDs', default=None)
    #
    parser.add_option('-o','--output',dest='output', type='string',default='map.nx', help='Output file. Reccomended to be .nx')
    #
    (options,args) = parser.parse_args()

    if options.nx == None:
        print("Please specify a .nx file produced with sumo2grid with --nx.")
        sys.exit(0)
    return options

def banner():
    msg = """
     ▐ ▄ ▐▄• ▄  ▄▄▄· .▄▄ ·  ▄▄▄·
    •█▌▐█ █▌█▌▪▐█ ▀█ ▐█ ▀. ▐█ ▄█
    ▐█▐▐▌ ·██· ▄█▀▀█ ▄▀▀▀█▄ ██▀·
    ██▐█▌▪▐█·█▌▐█ ▪▐▌▐█▄▪▐█▐█▪·•
    ▀▀ █▪•▀▀ ▀▀ ▀  ▀  ▀▀▀▀ .▀   .py
    
    NetworkX All Sortest Paths 
                                by Quentin Goss
    """
    print(msg)
    return

def read_graph():
    print("Loading networkx graph...",end='')
    g = nx.read_edgelist(OPTIONS.nx,data=(("weight",float),("id",str),),nodetype=str,comments='%',create_using=nx.MultiDiGraph())
    print("Complete!")
    return g
    
# Determines path weight
# @param nx.*Graph g = networkx graph
# @param [str] = path of node ids
# @return (float,[str]) = (weight,[edge ids])
def path_info(g,path):
    weight = 0.0
    for eid in range(1,len(path)):
        nxedges = g.get_edge_data(path[eid-1],path[eid])
        edge_weight = None
        for i in range(0,len(nxedges)):
            if edge_weight == None or nxedges[i]['weight'] < edge_weight:
                edge_weight = nxedges[i]['weight']
            continue
        weight += edge_weight
        continue
    return weight

if __name__ == "__main__":
    main()




















