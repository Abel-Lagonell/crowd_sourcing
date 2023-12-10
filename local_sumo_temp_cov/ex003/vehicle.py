# vehicle.py
# Author: Quentin Goss
# Last Modified: 10/17/1995
import random
import env
import networkx as nx
import nxops
import pantherine as purr
import preprocess
import numpy as np

# Adds a vehicle to the simulation
# @param traci = traci object
def add():
    # Vehicle ID
    index = env.veh_id_counter
    env.veh_id_counter += 1
    vid = "veh%d" % (index)
    
    # Retrieve Route
    veh = env.vehicles[index]
    
    # Create a route with the path eids
    rid = "route%d" % (env.route_id_counter)
    env.route_id_counter += 1
    env.traci.route.add(rid,veh['shortest path']['eids'])
    
    # Add a vehicle
    env.traci.vehicle.add(vid,rid)
    
    # Add the destination node to list of sink nodes so it may be found later
    dest_node = purr.filterdicts(env.nodes,'id',veh['shortest path']['nids'][-1])[0]
    env.vehicles_dest.append(dest_node)
    
    return

# Inititalizes the shortests path of all vehicles
def initialize():
    env.vehicles = [None for iveh in range(env.veh_total)]
    total = len(env.vehicles)
    for i, x in enumerate(env.vehicles):
        veh = vehdict()
        veh['id'] = 'veh%d' % (i)
        veh['shortest path'] = random_shortest_path()
        veh['source'] = veh['shortest path']['nids'][0]
        veh['destination'] = veh['shortest path']['nids'][-1]
        veh['shortest path length'] = veh['shortest path']['weight']
        env.vehicles[i] = veh
        purr.update(i+1,total,"Initializing Vehicles ")
    print()
    return

# Determines the spawn and sink node
# @return A random but valid shortest path
def random_shortest_path():
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
            print("Cannont create a path between %s and %s... Trying again (%d)." % (spawn_edge['from'],sink_edge['to'],ntrys))
        continue
        
    # At this point, it is assumed that the path is connected
    # Now the weight of the path and the edge eids of the path is determined
    shortest_path['weight'], shortest_path['eids'] = nxops.path_info(env.nx,shortest_path['nids'])
    
    return shortest_path

# Updates vehicle position and situation
def update():
    env.update_vehicle_info = False
    
    # Clean out the old object 
    env.vehicles_active = []
    
    # Refill 
    for i,vid in enumerate(env.traci.vehicle.getIDList()):
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
            
        # What is the weight of Veh --> Dest
        veh['veh2dest weight'] = veh['weight remaining'] + nxops.path_info(env.nx,nx.dijkstra_path(env.nx,veh['current edge']['to'],veh['destination node']['id']))[0]

        env.vehicles_active.append(veh)
        
        env.recalculate_nash = True
        continue
    return

def vehdict():
    veh = {
        'id':None,                   # Output
        'source':None,               # Output
        'destination':None,          # Output
        'shortest path length':None, # Output
        'diversion path length':None,# Output
        'sample time':None,          # Output
        'sample time diff':None,                  # Output
        'target nid':None,           # Output
        'target eid':None,
        'shortest path':None
    }
    return veh

# Checks if a vehicle has reached it's target
# @param string vid = vehicle ID
# @return True if vehicle is on it's target edge
def is_veh_at_target(vid):
    index = int(vid[3:])
    if env.vehicles[index]['target eid'] == env.traci.vehicle.getRoadID(vid):
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
            # Time since last sample
            if len(env.targets[itar]['sampling times']) == 0:
                dt = np.inf
            else:
                dt = n_step - env.targets[itar]['sampling times'][-1]
            env.vehicles[index]['sample time diff'] = dt
            env.targets[itar]['sampling times'].append(n_step)
            env.targets[itar]['sampling vids'].append(vid)
            s = {
                'target':env.targets[itar]['id'],
                'vehicle':vid,
                'time':n_step,
                'dt':dt
            }
            env.samples.append(s)
            print("\n%s: Sample taken at %s!" % (vid,tid))
            break
    return
    
# Writes the result of simulation to csv
def csv():
    print("Writing vehicles.csv...",end='')
    with open("%s/vehicles.csv" % (env.out_dir),'w') as f:
        f.write("id,source,destination,shortest.path.length,diversion.path.length,sample.time,sample.time.diff,target.id\n")
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
            if veh['sample time diff'] == None:
                f.write(',')
            else:
                f.write("%0f," % (veh['sample time diff']))
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
        f.write("%7s, %11s, %11s, %20s, %21s, %11s, %16s, %11s\n" % ("id","source", "destination", "shortest path length", "diversion path length", "sample time","sample time diff", "target id"))
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
            if veh['sample time diff'] == None:
                f.write(" %16s" % (''))
            elif veh['sample time diff'] == np.inf:
                f.write(" %16s" % ("Inf"))
            else:
                f.write(" %16d" % (veh['sample time diff']))
            if veh['target nid'] == None:
                f.write("\n")
            else:
                f.write(" %11s\n" % (veh['target nid']))
            continue
    print("Complete!")
    return
