# polygon.py
# Author: Quentin Goss
# Methods for making polygons
import env

# Add a polygon
# @param [(x,y),...] shape = shape of the polygon
# @param (red,green,blue) color = color of the polygon
# @param int layer = layer
# @param fill = Fill in shape when true
# @return polygon ID
def add(shape,color,layer,fill=True):
    sid = 'poly%d' % (len(env.traci.polygon.getIDList())+1)
    env.traci.polygon.add(sid,shape,color=color,layer=layer,fill=fill)
    return sid
