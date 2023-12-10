# nash.py
# Author: Quentin Goss
import pantherine as purr
import env
import vehicle
import systematicSim as sysSim
import numpy as np
import nxops

# Recalculate the nash equation.
def recalculate():
    env.recalculate_nash = False
    print()
    
    print("Retrieving spatial vehicle data...",end='')
    st = purr.now()
    vehicle.update_nash()
    print("Complete after %.3fs" % (purr.elapsed(st)))
    
    print("Recalculating target assignments...",end='')
    st = purr.now()
    N=len(env.vids_active)-1
    # ~ N = 10
    env.nash_assigner = sysSim.nashAssigner(N=N,M=len(env.targets),R=200,tau=1,dist=env.dist)
    t = env.nash_assigner.getAssignments()
    print("Complete after %.3fs" % (purr.elapsed(st)))
    
    cDest = t[0] 
    utilities = t[1]

    # ~ print('Assigining vehicles to new targets.')
    for x in range(env.nash_assigner.N):
        # ~ print('vehicle,target,utililty: (%d,%.0f,%.3f)'%(x,cDest[x],utilities[x]))
        
        veh = env.vehicles_active[x]
        path = dict()
        
        # Not worth the effort. Go home
        if np.isnan(cDest[x]):
            path['nids'] = nxops.dijkstra(env.nx,veh['current edge']['to'],veh['destination node']['id'])
            path['nids'].insert(0,veh['current edge']['from'])
            path['weight'] , path['eids'] = nxops.path_info(env.nx,path['nids'])
            
        # Otherwise, go to the target
        else:
            # Path veh --> target
            path_veh2tar = dict()
            tar = env.target_nodes[int(cDest[x])]
            path_veh2tar['nids'] = nxops.dijkstra(env.nx,veh['current edge']['to'],tar['id'])
            path_veh2tar['nids'].insert(0,veh['current edge']['from'])
            path_veh2tar['weight'] , path_veh2tar['eids'] = nxops.path_info(env.nx,path_veh2tar['nids'])
            
            # path target --> dest
            path_tar2dest = dict()
            path_tar2dest['nids'] = nxops.dijkstra(env.nx,tar['id'],veh['destination node']['id'])
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
        
        
        
        # Route the vehicle with traci
        env.traci.vehicle.setRoute(veh['id'],path['eids'])
        continue
        
    # ~ print('Dijkstra: Calls=%d Time=%.3fs Avg=%.3fs' % (env.fs_dijkstra['calls'],env.fs_dijkstra['time'],env.fs_dijkstra['time']/env.fs_dijkstra['calls']))
    
    return
