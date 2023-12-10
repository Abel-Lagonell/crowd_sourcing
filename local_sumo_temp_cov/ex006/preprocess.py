# preprocess.py
# Author: Quentin Goss
# Preprocessing steps are kept in this file
import env
import pantherine as purr
import networkx as nx
import os
import sys
    
# Creates a polygon for visualization of spawn/sink radius
# @param traci = Traci object
# @param (float,float) point = (x,y) point
# @param float radius = radius around point
# @param (int,int,int,int) color = RGBA color
# @param int layer = layer
def add_radius_polygon(point,radius,color,layer=0):
    x,y = point
    pid = 'poly%d' % (len(env.traci.polygon.getIDList())+1)
    shape = [(x-radius,y-radius),(x-radius,y+radius),(x+radius,y+radius),(x+radius,y-radius)]
    env.traci.polygon.add(pid,shape,color,fill=True,layer=layer)
    return

# Intitialize the edge and node structures
def initialize_edges_and_nodes():
    print("Loading edges and nodes...",end="")
    edg_xml = purr.mrf(env.options.map_dir,r'*.edg.xml')
    env.edges = purr.readXMLtag(edg_xml,'edge')
    nod_xml = purr.mrf(env.options.map_dir,r'*.nod.xml')
    env.nodes = purr.readXMLtag(nod_xml,'node')
    print("Complete!")
    return

# Loads the networkx graph
def initialize_nx():
    print("Loading networkx graph...",end='')
    map_nx = purr.mrf(env.options.map_dir,r'*.nx')
    env.nx = nx.read_edgelist(map_nx,data=(("weight",float),("id",str),),nodetype=str,comments='%',create_using=nx.MultiDiGraph())
    print("Complete!")
    return

