# vehicle.py
# Author: Quentin Goss
# Last Modified: 10/17/1995
import random
import env
import networkx as nx
import nxops
import pantherine as purr
import preprocess

# Adds a vehicle to the simulation
# @param traci = traci object
def add(traci):
    if env.method == 'baseline':
        add_baseline(traci)
    elif env.method == 'nash':
        add_nash(traci)
    else:
        raise(ValueError)
    return

def add_baseline(traci):
    # Vehicle ID
    vid = "veh%d" % (env.veh_id_counter)
    env.veh_id_counter += 1

    # Selected a path. It must be have a conenction between spawn and sink
    ntrys = 0; shortest_path = {'weight':None,'nids':None,'eids':None}
    while True:
        # Pick a random spawn and sink edge
        spawn_edge = random.choice(env.spawn_edge)
        sink_edge = random.choice(env.sink_edge)
        
        # Determine the shortest path
        try:
            shortest_path['nids'] = nx.dijkstra_path(env.nx,spawn_edge['from'],sink_edge['to'])
            break
        except nx.NetworkXNoPath:
            ntrys += 1
            print("%s: Cannont create a path between %s and %s... Trying again (%d)." % (vid,spawn_edge['from'],sink_edge['to'],ntrys))
        continue
        
    # At this point, it is assumed that the path is connected
    # Now the weight of the path and the edge eids of the path is determined
    shortest_path['weight'], shortest_path['eids'] = nxops.path_info(env.nx,shortest_path['nids'])
    
    # display the spawn and sink destions
    spawn_node,sink_node = purr.flattenlist(purr.batchfilterdicts(env.nodes,'id',[shortest_path['nids'][0],shortest_path['nids'][-1]]))
    spawn_point = (float(spawn_node['x']),float(spawn_node['y']))
    sink_point = (float(sink_node['x']),float(sink_node['y']))
    
    # Find the optimal target point to visit
    path = nxops.naive_target_selection(env.nx,shortest_path['nids'],env.target_nodes)
    
    # Create a route with the path eids
    rid = "route%d" % (env.route_id_counter)
    env.route_id_counter += 1
    traci.route.add(rid,path['path_eids'])
    
    # Add a vehicle
    traci.vehicle.add(vid,rid)
    
    # Determine the edge immediately after the node
    target_node_index = path['path_nids'].index(path['target_node']['id'])
    target_eid = path['path_eids'][target_node_index]
    
    # Create the vehicle dictionary
    veh = {
        "id":vid,
        "source":spawn_node['id'],
        "destination":sink_node['id'],
        "shortest path length":shortest_path['weight'],
        "diversion path length":path['weight'],
        "sample time":None,
        "target nid":path['target_node']['id'],
        "target eid":target_eid,
        "path":path
    }
    env.vehicles.append(veh)
    return

def add_nash(traci):
    # Vehicle ID
    vid = "veh%d" % (env.veh_id_counter)
    env.veh_id_counter += 1

    # Selected a path. It must be have a conenction between spawn and sink
    ntrys = 0; shortest_path = {'weight':None,'nids':None,'eids':None}
    while True:
        # Pick a random spawn and sink edge
        spawn_edge = random.choice(env.spawn_edge)
        sink_edge = random.choice(env.sink_edge)
        
        # Determine the shortest path
        try:
            shortest_path['nids'] = nxops.dijkstra(env.nx,spawn_edge['from'],sink_edge['to'])
            break
        except nx.NetworkXNoPath:
            ntrys += 1
            print("%s: Cannont create a path between %s and %s... Trying again (%d)." % (vid,spawn_edge['from'],sink_edge['to'],ntrys))
        continue
    shortest_path['weight'], shortest_path['eids'] = nxops.path_info(env.nx,shortest_path['nids'])
    
    # Create a route with the path eids
    rid = "route%d" % (env.route_id_counter)
    env.route_id_counter += 1
    traci.route.add(rid,shortest_path['eids'])
    
    # Add a vehicle
    traci.vehicle.add(vid,rid)
    
    # Add the destination node to list of sink nodes so it may be found later
    dest_node = purr.filterdicts(env.nodes,'id',shortest_path['nids'][-1])[0]
    env.vehicles_dest.append(dest_node)
    
    # The nash equilibrium will have to be recalculated since another contestant is being introduced.
    env.recalculate_nash = True
    
    # Create the vehicle dictionary
    veh = {
        "id":vid,
        "source":spawn_edge['from'],
        "destination":sink_edge['to'],
        "shortest path length":shortest_path['weight'],
        "diversion path length":None,
        "sample time":None,
        "target nid":None,
        "target eid":None
    }
    env.vehicles.append(veh)
    
    return

# Checks if a vehicle has reached it's target
# @param traci = traci object
# @param string vid = vehicle ID
# @return True if vehicle is on it's target edge
def is_veh_at_target(traci,vid):
    index = int(vid[3:])
    if env.vehicles[index]['target eid'] == traci.vehicle.getRoadID(vid):
        return True
    return False

# Take a sample
# @param string vid = vehicle ID
# @param int n_step = Current timestep
def sample(vid,n_step):
    index = int(vid[3:])
    # Sample only once
    if not env.vehicles[index]['sample time'] == None:
        return
    # Record time
    env.vehicles[index]['sample time'] = n_step
    # Track the sample time on the target too
    tid = env.vehicles[index]['target nid']
    for itar in range(0,len(env.targets)):
        if env.targets[itar]['id'] == tid:
            env.targets[itar]['sampling times'].append(n_step)
            env.targets[itar]['sampling vids'].append(vid)
            print("\n%s: Sample taken at %s!" % (vid,tid))
            break
    
    if env.method == 'nash':
        env.recalculate_nash = True
    return

# Writes the result of simulation to csv
def csv():
    print("Writing vehicles.csv...",end='')
    with open("%s/vehicles.csv" % (env.out_dir),'w') as f:
        f.write("id,source,destination,shortest path length,diversion path length,sample time,target id\n")
        for veh in env.vehicles:
            f.write("%s,%s,%s,%.3f," % (veh['id'],veh['source'],veh['destination'],veh['shortest path length']))
            if veh['diversion path length'] == None:
                f.write(",")
            else:
                f.write("%.3f," % (veh['diversion path length']))
            if veh['sample time'] == None:
                f.write(",")
            else:
                f.write("%d," % (veh['sample time']))
            if veh['target nid'] == None:
                f.write("\n")
            else:
                f.write("%s\n" % (veh['target nid']))
            continue
    print("Complete!")
    return

# Pretty output
def out_pretty():
    print("Writing pretty vehicle output...",end='')
    with open("%s/vehicles.pretty" % (env.out_dir),'w') as f:
        f.write("%7s, %11s, %11s, %20s, %21s, %11s, %s\n" % ("id","source", "destination", "shortest path length", "diversion path length", "sample time", "target id"))
        for veh in env.vehicles:
            f.write("%7s, %11s, %11s, %20.3f," % (veh['id'],veh['source'][:11],veh['destination'][:11],veh['shortest path length']))
            if veh['diversion path length'] == None:
                f.write(" %21s," % (''))
            else:
                f.write(" %21.3f," % (veh['diversion path length']))
            if veh['sample time'] == None:
                f.write(" %11s," % (''))
            else:
                f.write(" %11d," % (veh['sample time']))
            if veh['target nid'] == None:
                f.write("\n")
            else:
                f.write(" %s\n" % (veh['target nid']))
            continue
    print("Complete!")
    return

# Updates the vehicles_active list
#  This should be called when the nash equilibrium is recalculated, before the nashAssigner
def update_nash():
    
    # Clean out the old object 
    env.vehicles_active = []
    
    # Refill 
    for i,vid in enumerate(env.vids_active):
        veh = dict()
            
        # Who am I?
        veh['id'] = vid
        
        # Where am I?
        veh['route index'] = env.traci.vehicle.getRouteIndex(veh['id'])
        
        # What is my route?
        veh['route id'] = env.traci.vehicle.getRouteID(veh['id'])
        
        # What is my sink node?
        veh['destination node'] = env.vehicles_dest[int(veh['id'][3:])]
        
        # How far along the edge am I (m)?
        veh['position on edge (m)'] = env.traci.vehicle.getLanePosition(veh['id'])
        
        # What edge am I on?
        eid = env.traci.vehicle.getRoadID(veh['id'])
        
        
        # Obtain the edge object. Here we can have two cases:
        #  1. veh is at an intersection
        #  2. veh is on an edg
        
        # Veh is within an intersection. Assume the start of the next edge with a position on edge (m) of zero.
        if ':' in eid:
            veh['route'] = env.traci.route.getEdges(veh['route id'])
            eid = veh['route'][veh['route index']+1]
            veh['current edge'] = purr.filterdicts(env.edges,'id',eid)[0]
            veh['position on edge (m)'] = 0.000001
        else:
            veh['current edge'] = purr.filterdicts(env.edges,'id',eid)[0]
            
        # How far am I along the edge (weight)
        veh['position on edge (s)'] = veh['position on edge (m)'] / float(veh['current edge']['speed'])
            
        # How much weight to the end of the edge?
        edge_candidates = env.nx.get_edge_data(veh['current edge']['from'],veh['current edge']['to'])
        for i in range(len(edge_candidates)):
            if veh['current edge']['id'] == edge_candidates[i]['id']:
                veh['weight remaining'] = edge_candidates[i]['weight'] - veh['position on edge (s)']
                break
            continue

        env.vehicles_active.append(veh)
        continue
        
    # ~ print('active vehicles',len(env.vehicles_active))
    return
