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

# Initilizes targets with a conical spread between the two spawn/sink points
# @return Chosen Targets
def cone_spread():
    cones = cone_target_region()
    target_node_candidates = []
    total = len(env.nodes) - 1
    for n, node in enumerate(env.nodes):
        x = float(node['x'])
        y = float(node['y'])
        for shape in cones:
            if purr.point_inside_polygon(x,y,shape):
                target_node_candidates.append(node)
                break
            continue
        purr.update(n,total,"Finding target node candidates ")
        continue
    print()
    print('Found %d target node candidates.' % (len(target_node_candidates)))
    if env.target_n > len(target_node_candidates):
        print("Not enough nodes for requested target amount. Increase target.node.angle.")
        sys.exit(1)
    random.seed(env.seed)
    return random.sample(target_node_candidates,env.target_n)

# Get the region where targets may spawn.
# This is defined by a bi-directional triangular trajectory given a hypotenuse length an angle theta
# @return The shapes of the four triangles
def cone_target_region():
    # The triangle between spawn and sink
    adj = env.point_spawn[0] - env.point_sink[0]
    opp = env.point_spawn[1] - env.point_sink[1]
    s2s = purr.triangle(adj=adj,opp=opp,p0=env.point_spawn,rotation=270,aflip=True)
    
    # A Form a cone from the center of the hypotenuse
    x0,y0 = env.point_spawn; x1,y1 = env.point_sink
    p0 = ((x0+x1)/2,(y0+y1)/2)
    hyp = env.target_cone_size
    theta = env.target_cone_angle
    rotation = s2s['theta'] + 90
    
    cone0 = purr.triangle(hyp=hyp,theta=theta,p0=p0,rotation=rotation)
    shape_c0 = [cone0['p0'],cone0['p1'],cone0['p2']]
    polygon.add(shape_c0,(255,255,0),2)
    
    cone1 = purr.triangle(hyp=hyp,theta=theta,p0=p0,rotation=rotation,aflip=True)
    shape_c1 = [cone1['p0'],cone1['p1'],cone1['p2']]
    polygon.add(shape_c1,(220,220,0),2)
    
    cone2 = purr.triangle(hyp=hyp, theta=theta, p0=p0, rotation=rotation+180)
    shape_c2 = [cone2['p0'],cone2['p1'],cone2['p2']]
    polygon.add(shape_c2,(255,255,0),2)
    
    cone3 = purr.triangle(hyp=hyp, theta=theta, p0=p0, rotation=rotation+180,aflip=True)
    shape_c3 = [cone3['p0'],cone3['p1'],cone3['p2']]
    polygon.add(shape_c3,(220,220,0),2)
    
    return (shape_c0,shape_c1,shape_c2,shape_c3)

# Intitialize targets, generating a list of target node dictionary
#  objects which are store in env.target_nodes
#  The targets file should contain the ids of nodes in the network,
#  one node id per line. Lines with % are ignored
def initialize(traci):    
    # Load targets from file
    if not env.target_file == None:
        print("Loading targets from file \"%s\"." % (env.target_file))
        env.target_nodes = purr.readJSON(env.target_file)
    # Otherwise use cone spread
    else:    
        env.target_nodes = cone_spread()
        purr.save("temp/targets.json",env.target_nodes)
        if env.target_generate:
            print("Target's Generated. Exiting. Check temp/targets.json for targets.")
            sys.exit(0)
    
    # Mark the targets on the map
    for node in env.target_nodes:
        xy = (float(node['x']),float(node['y']))
        preprocess.add_radius_polygon(traci,xy,30,(255,153,204),layer=3)
    
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
