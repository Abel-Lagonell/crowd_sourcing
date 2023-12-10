# nash.py
# Author: Quentin Goss

import pantherine as purr
import env
import systematicSim as sysSim
import numpy as np
import nxops
import networkx as nx

def get_assignments():
    print("\nGetting Nash Assignments.")
    start = purr.now()
    
    # Get assigments
    index = env.traci.vehicle.getIDCount() - 1
    t = env.nash_assigners[index].getAssignments()
    cDest = t[0] 
    utilities = t[1]
    
    
    # Use this info to route.
    for x in range(env.nash_assigners[index].N):
        print('Veh=%d Tar=%.0f Util=%.3f'%(x,cDest[x],utilities[x]))
        
        veh = env.vehicles_active[x]
        path = dict()
        
        # Not worth the effort. Go home
        if np.isnan(cDest[x]):
            path['nids'] = nx.dijkstra_path(env.nx,veh['current edge']['to'],veh['destination node']['id'])
            path['nids'].insert(0,veh['current edge']['from'])
            path['weight'] , path['eids'] = nxops.path_info(env.nx,path['nids'])
            
        # Otherwise, go to the target
        else:
            # Path veh --> target
            path_veh2tar = dict()
            tar = env.target_nodes[int(cDest[x])]
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
        
    print("Complete after %.3f" % (purr.elapsed(start)))
    return

# Create a new assigner
# @param int N = Number of Vehicles to Consider
def new_assigner(N):
    M = len(env.target_nodes)
    nash_assigner = sysSim.nashAssigner(N,M,env.R,env.tau,dist=env.dist)
    return nash_assigner

# Create a list of assigners, where N=1 to N=veh.exists.max
def initialize():
    env.nash_assigners = []
    for i in range(1,env.veh_exists_max + 1):
        env.nash_assigners.append(new_assigner(i))
    return
