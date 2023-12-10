# nxopy.py
# Author: Quentin Goss
# Performs common network x operations
import networkx as nx
import pantherine as purr
import env

# Determines path weight and the edge ids of the edges along the path
# @param nx.*Graph g = networkx graph
# @param [str] = path of node ids
# @return (float,[str]) = (weight,[edge ids])
def path_info(g,path):
    weight = 0.0
    eids = []
    for eid in range(1,len(path)):
        nxedges = g.get_edge_data(path[eid-1],path[eid])
        edge_weight = None
        shortest_eid = None
        for i in range(0,len(nxedges)):
            if edge_weight == None or nxedges[i]['weight'] < edge_weight:
                edge_weight = nxedges[i]['weight']
                shortest_eid = nxedges[i]['id']
            continue
        weight += edge_weight
        eids.append(shortest_eid)
        continue
    return (weight,eids)
    
# A new path dictionary
def new_path():
    return {'weight':None,'path_eids':None,'target_node':None,'path_nids':None}
