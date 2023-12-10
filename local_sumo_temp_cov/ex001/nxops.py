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

# Selects a new path to one of the targets, which is the target that diverges least from it's path.
# @param nx.*Graph g = networkx graph
# @param [str] shortest_path = Path of node ids of the shortest path
# @param [dict] target_nodes = SUMO node dictionaries of target nodes
# @param dict best_path = The optimal path.
def naive_target_selection(g,shortest_path,target_nodes):
    best_path = new_path()
    for target_node in target_nodes:
        # Determine target path weight
        seg1 = nx.dijkstra_path(g,shortest_path[0],target_node['id'])
        seg2 = nx.dijkstra_path(g,target_node['id'],shortest_path[-1])
        seg1.extend(seg2[1:])
        weight,path_eids = path_info(g,seg1)
        
        # If the weight is better, select it.
        if best_path['weight'] == None or weight < best_path['weight']:
            best_path['weight'] = weight
            best_path['path_eids'] = path_eids
            best_path['target_node'] = target_node
            best_path['path_nids'] = seg1
        continue
    return best_path

# A new path dictionary
def new_path():
    return {'weight':None,'path_eids':None,'target_node':None,'path_nids':None}

# Determines shortest path using dijkstra
# @param nx g = networkx graph
# @param string node_from = nid of start node
# @param string node_to = nid of end node
# @return (str,...) = Path of nids
def dijkstra(g,node_from,node_to):
    st = purr.now()
    path = nx.dijkstra_path(g,node_from,node_to)
    env.fs_dijkstra['calls'] += 1
    env.fs_dijkstra['time'] += purr.elapsed(st)
    return path

# Lookup path weight from table
# @param str nid_from = ID of origin node
# @param str nid_to = ID of destination node
# @return float weight of shortest path
def lookup_weight(nid_from,nid_to):
    ifrom = purr.binsearch(env.nid2spwid_sids,purr.ascii2int(nid_from))
    ito = purr.binsearch(env.nid2spwid_sids,purr.ascii2int(nid_to))
    return env.shortest_path_weights[ifrom][ito]
