# targets.py
# Author: QuentinGoss
import preprocess
import pantherine as purr
import os
import sys
import env
import math
import pantherine as purr
import polygon
import random

# Intitialize targets, generating a list of target node dictionary
#  objects which are store in env.target_nodes
#  The targets file should contain the ids of nodes in the network,
#  one node id per line. Lines with % are ignored
def initialize(traci):    
    env.target_nodes = env.tP
    
    # Mark the targets on the map
    for node in env.target_nodes:
        xy = (float(node['x']),float(node['y']))
        preprocess.add_radius_polygon(xy,50,(0,255,0),layer=3)
        preprocess.add_radius_polygon(xy,10,(255,255,0),layer=4)
    
    # Add target dictionaries to the env
    for node in env.target_nodes:
        target = {
            'id':node['id'],
            'sampling times':[],
            'sampling vids':[]
        }
        env.targets.append(target)
        continue
    
    print("Complete!")
    return

# Writes the result of the simulation to csv
def csv():
    print("Writing targets.csv...",end='')
    with open("%s/targets.csv" % (env.out_dir),'w') as f:
        f.write('target,vehicle,time,dt\n')
        for sample in env.samples:
            f.write('%s,%s,%d,%0f\n' % (sample['target'],sample['vehicle'],sample['time'],sample['dt']))
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
