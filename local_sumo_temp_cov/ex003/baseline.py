# Baseline.py
# Author: Quentin Goss
# Baseline method functionaility
import pantherine as purr
import env
import networkx as nx
import nxops

def assign():
    print('\nBaseline Assignments')
    
    N = env.traci.vehicle.getIDCount()
    M = len(env.target_nodes)
    for n in range(N):
        # Determine which target is the least far away
        cost = [float(env.dist.cost(n,m)) for m in range(M)]
        min_cost = min(cost)
        itar = None
        for i,c in enumerate(cost):
            if c == min_cost:
                itar = i
                break
            continue
        print("Veh=%d Tar=%d Cost=%.3f" % (n,itar,min_cost))
            
        # Then assign the route
        veh = env.vehicles_active[n]
        path = dict()
        
        # Path veh --> target
        path_veh2tar = dict()
        tar = env.target_nodes[itar]
        path_veh2tar['nids'] = nx.dijkstra_path(env.nx,veh['current edge']['to'],tar['id'])
        path_veh2tar['nids'].insert(0,veh['current edge']['from'])
        path_veh2tar['weight'] , path_veh2tar['eids'] = nxops.path_info(env.nx,path_veh2tar['nids'])
        
        # path target --> dest
        path_tar2dest = dict()
        path_tar2dest['nids'] = nx.dijkstra_path(env.nx,tar['id'],veh['destination node']['id'])
        path_tar2dest['weight'], path_tar2dest['eids'] = nxops.path_info(env.nx,path_tar2dest['nids'])
        
        # Combine together
        path['nids'] = purr.flattenlist([path_veh2tar['nids'],path_tar2dest['nids']])
        path['weight'] = path_veh2tar['weight'] + path_tar2dest['weight']
        path['eids'] = purr.flattenlist([path_veh2tar['eids'],path_tar2dest['eids']])
        
        # Update vehicle tracking data
        index = int(veh['id'][3:])
        env.vehicles[index]['target nid'] = tar['id']
        env.vehicles[index]['target eid'] = path['eids'][path['nids'].index(tar['id'])]
        env.vehicles[index]['diversion path length'] = path['weight']
        env.vehicles[index]['shortest path length'] = veh['veh2dest weight']
        
        # Route the vehicle with traci
        env.traci.vehicle.setRoute(veh['id'],path['eids'])
        
        continue
    
    print("Complete!")
    return
