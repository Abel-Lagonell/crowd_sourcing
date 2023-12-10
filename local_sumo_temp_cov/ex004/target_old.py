# targets.py
# Author: QuentinGoss
import preprocess
import pantherine as purr
import os
import sys
import env
import math
import pantherine as purr

# Initilizes targets with a conical spread between the two spawn/sink points
def cone_spread():
    # Between Spawn and Source Centers
    s2s = triangle(env.point_spawn,env.point_sink,color=(0,255,255),layer=1)
    
    # The midpoint between spawn and source
    p0 = ((s2s['p0'][0] + s2s['p1'][0])/2,(s2s['p0'][1] + s2s['p1'][1])/2)
    p1 = (s2s['p0'][0] + s2s['opp'],s2s['p0'][1])
    midpoint = triangle(p0,p1,color=(255,255,0),layer=2)
    
    # Make a cone from the center of that line
    m = 15
    angle = math.degrees(math.atan(midpoint['opp']/midpoint['adj']))
    theta = 90 - angle + m
    adj = 3000
    opp = hyp * math.sin(math.radians(theta))
    print('angle=%.2f, theta=%.2f, hyp=%.2f, adj=%.2f, opp=%.2f' % (angle,theta,hyp,adj,opp))
    
    # Create a new triangle
    p0 = midpoint['p0']
    p1 = (midpoint['p0'][0] - opp, midpoint['p0'][1] + adj)
    cone1 = triangle(p1,p0,color=(255,0,255),layer=1)
    
    return

# Creates a right triangle dict given two points and a color
# @param (float, float) p0 = (x,y) point 0
# @param (float, float) p1 = (x,y) point 1
# @param (int,int,int) color = (red,blue,green) color
# @param int layer = layer to be displayed
# @return triangle dictionary
#            .(x1,y1)
#           /|
#      hyp / | adj
#         /__|
# (x0,y0)` opp
def triangle(p0,p1,color,layer):
    x0 = p0[0]; y0 = p0[1]
    x1 = p1[0]; y1 = p1[1]
    opp = abs(x0-x1)
    adj = abs(y0-y1)
    hyp = math.sqrt(math.pow(opp,2) + math.pow(adj,2))
    sid = 'poly%d' % (len(env.traci.polygon.getIDList())+1)
    shape = [(x0,y0),(x1,y1),(x0+opp,y0)]
    env.traci.polygon.add(sid,shape,color=color,layer=layer,fill=True)
    tr = {
        'p0':p0,
        'p1':p1,
        'opp':opp,
        'adj':adj,
        'hyp':hyp,
        'id':sid,
    }
    return tr

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
