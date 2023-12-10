# targets.py
# Author: QuentinGoss
import preprocess
import pantherine as purr
import os
import sys
import env

# Intitialize targets, generating a list of target node dictionary
#  objects which are store in env.target_nodes
#  The targets file should contain the ids of nodes in the network,
#  one node id per line. Lines with % are ignored
def initialize(traci):
    print("Initializing targets...",end='')
    # load the node target IDs from file.
    target_node_ids = []
    try:
        with open(env.options.targets,'r') as f:
            for line in f:
                if '%' in line:
                    continue
                target_node_ids.append(line.strip())
                continue
    except FileNotFoundError:
        print('\nCould not open "%s"' % (env.options.targets))
        sys.exit(1)
    
    # Then retrieve the nodes
    env.target_nodes = purr.flattenlist(purr.batchfilterdicts(env.nodes,'id',target_node_ids))
    
    # Mark the targets on the map
    for node in env.target_nodes:
        xy = (float(node['x']),float(node['y']))
        preprocess.add_radius_polygon(traci,xy,30,(255,0,255))
    
    # Add target dictionaries to the env
    for node in env.target_nodes:
        target = {
            'id':node['id'],
            'sampling times':[],
            'sampling vids':[]
        }
        # ~ for i in range(0,env.veh_total):
            # ~ target['sampling times'].append(None)
        env.targets.append(target)
        continue
    
    print("Complete!")
    return

# Writes the result of the simulation to csv
def csv():
    print("Writing targets.csv...",end='')
    with open("%s/targets.csv" % (env.out_dir),'w') as f:
        f.write("id")
        for i in range(0,env.veh_total):
            f.write(",veh%d" % (i))
        f.write("\n")
        for target in env.targets:
            f.write("%s" % target['id'])
            for val in target["sampling times"]:
                f.write(",")    
                if not val == None:
                    f.write("%d" % (val))
                continue
            f.write("\n")
            continue
    print("Complete!")
    return

# Writes the results of the simulation to json
def json():
    print("Writing targets.json...",end='')
    purr.save("%s/targets.json" % (env.out_dir),env.targets)
    print("Complete!")
    return
    
def out_pretty():
    print("Writing pretty target output...",end='')
    with open("%s/targets.pretty" % (env.out_dir),'w') as f:
        for target in env.targets:
            f.write("%s\n" % (target['id']))
            f.write("sampling times: ")
            for st in target["sampling times"]:
                f.write("%7d, " % (st))
            f.write("\n")
            f.write(" sampling vids: ")
            for vid in target["sampling vids"]:
                f.write("%7s, " % (vid))
            f.write("\n\n")
            continue
    return
