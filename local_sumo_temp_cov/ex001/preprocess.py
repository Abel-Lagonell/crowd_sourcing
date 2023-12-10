# preprocess.py
# Author: Quentin Goss
# Preprocessing steps are kept in this file
import env
import pantherine as purr
import networkx as nx
import os
import sys

# Finds valid edges around an point
# @param (float,float) point = (x,y) point
# @param float radius = radius around point
# @return [dict] = a list of edge dictionaries
def get_valid_edges_from_point(point,radius):
    print("Finding valid edges for point",point,"and radius",radius)
    x,y = point
    
    
    # Find the nodes that are within the radius
    nod_xml = purr.mrf(env.options.map_dir,r'*.nod.xml')
    nodes_all = purr.readXMLtag(nod_xml,'node')
    nodes_valid = []
    for node in nodes_all:        
        if abs(x - float(node['x'])) <= radius and abs(y - float(node['y'])) <= radius:
            nodes_valid.append(node)
        continue
        
    nodes_valid_ids = [node['id'] for node in nodes_valid]
    
    # Now that we know the nodes, we can pick out valid edges that the node begins at
    edg_xml = purr.mrf(env.options.map_dir,r'*.edg.xml')
    edges_all = purr.readXMLtag(edg_xml,'edge')
    edges_filtered = purr.batchfilterdicts(edges_all,'from',nodes_valid_ids,show_progress=True)
    edges_filtered = purr.flattenlist(edges_filtered)
    edges_valid = []
    for edge in edges_filtered:
        if not ':' in edge['id']:
            edges_valid.append(edge)
    
    print("Found %d edge candidates." % (len(edges_valid)))
    
    return edges_valid
    
# Creates a polygon for visualization of spawn/sink radius
# @param traci = Traci object
# @param (float,float) point = (x,y) point
# @param float radius = radius around point
# @param (int,int,int,int) color = RGBA color
def add_radius_polygon(traci,point,radius,color):
    x,y = point
    pid = 'poly%d' % (len(traci.polygon.getIDList())+1)
    shape = [(x-radius,y-radius),(x-radius,y+radius),(x+radius,y+radius),(x+radius,y-radius)]
    traci.polygon.add(pid,shape,color,fill=True,layer=1)
    return

# Intitialize the edge and node structures
def initialize_edges_and_nodes():
    edg_xml = purr.mrf(env.options.map_dir,r'*.edg.xml')
    env.edges = purr.readXMLtag(edg_xml,'edge')
    nod_xml = purr.mrf(env.options.map_dir,r'*.nod.xml')
    env.nodes = purr.readXMLtag(nod_xml,'node')
    return

# Selects edges for spawn and sink locations, draws rectangles to show region selction, and initilializes sink edge spawn routes.
# @param traci = Traci Object
def initialize_edges_for_spawns_and_sinks(traci):
    print("Initializeing edges/nodes.")
    initialize_edges_and_nodes()
    
    print("Finding spawn edge candidates.")
    if not os.path.exists('temp'):
        os.mkdir('temp')
    generate_spawns = True
    try:
        env.spawn_edge, last_spawn_point = purr.load('temp/spawns.bin')
        if last_spawn_point == env.point_spawn:
            generate_spawns = False
    except FileNotFoundError:
        pass
    if generate_spawns:
        env.spawn_edge = get_valid_edges_from_point(env.point_spawn,env.radius_spawn_sink)
        purr.save('temp/spawns.bin',[env.spawn_edge,env.point_spawn])
    add_radius_polygon(traci,env.point_spawn,env.radius_spawn_sink,(0,255,0))
    
    print("Finding sink edge candidates.")
    generate_sinks = True
    try:
        env.sink_edge,last_sink_point = purr.load('temp/sinks.bin')
        if last_sink_point == env.point_sink:
            generate_sinks = False
    except FileNotFoundError:
        pass
    if generate_sinks:
        env.sink_edge = get_valid_edges_from_point(env.point_sink,env.radius_spawn_sink)
        purr.save('temp/sinks.bin',[env.sink_edge,env.point_sink])
    add_radius_polygon(traci,env.point_sink,env.radius_spawn_sink,(255,0,0))
    return

# Loads the networkx graph
def initialize_nx():
    print("Loading networkx graph...",end='')
    map_nx = purr.mrf(env.options.map_dir,r'*.nx')
    env.nx = nx.read_edgelist(map_nx,data=(("weight",float),("id",str),),nodetype=str,comments='%',create_using=nx.MultiDiGraph())
    print("Complete!")
    return

# Load the shortest path weight matrix
def initialize_shortest_path_weights():
    _file = purr.mrf(env.options.map_dir,r'*.weight.pybin')
    env.shortest_path_weights = purr.load(_file)
    nodes = []   
    for i,nid in enumerate(list(env.nx.nodes)):
        nodes.append({"id":nid,"spw index":i,"sort id":purr.ascii2int(nid)})
    env.nid2spwid = purr.sortdicts(nodes,'sort id')
    env.nid2spwid_sids = [item['sort id'] for item in env.nid2spwid]
    return

