# distance.py
# Author: Quentin Goss
import networkx as nx
import pantherine as purr
import env
import nxops
import networkx as nx
import numpy as np
import datetime as dtime

#define class for distance function 
class distance: 
    def __init__(self):
        return

    # Determines the distance (in seconds) between a start and end point
    # @param int vehicle = index of vehicle
    # @param int target = index of target
    # @param bool source = 
    #       When false, return distance between target and destination. When true
    #       When true, return distance between vehicle current poisition and target
    # @return float distance
    def travelTime(self,vehicle,target,source):
        iveh = vehicle; itar = target
            
        # ~ if iveh == len(env.vehicles_active)-1 or iveh == 0:
            # ~ print('index of veh:',iveh,'| # of active veh:',len(env.vehicles_active))
            
        # Retrieve Vehicle and Target Data
        try:
            veh = env.vehicles_active[iveh]
        except IndexError:
            print('distance.py::33 Catching Index Error: iveh=',iveh)
            veh = env.vehicles_active[len(env.vehicles_active)-1]
        tar = env.target_nodes[itar]
        
        if source:          
            weight = veh['weight remaining'] + nxops.lookup_weight(veh['current edge']['to'],tar['id'])  
            
            # Determine the path with dijkstra. This is the path that starts from the node which the vehicle is currently moving along.
            # ~ path = nxops.dijkstra(env.nx,veh['current edge']['to'],tar['id'])
            
            # Add the distance to complete the current edge to the weight of the planned path.
            # ~ weight = veh['weight remaining'] + nxops.path_info(env.nx,path)[0]
            
        else:
            weight = nxops.lookup_weight(tar['id'],veh['destination node']['id'])
            
            # Determine the path with dijkstra. This is the path that starts from the target and ends at the vehicle destination
            # ~ path = nxops.dijkstra(env.nx,tar['id'],veh['destination node']['id'])
            
            # Determine the weight of the path
            # ~ weight = nxops.path_info(env.nx,path)[0]
        
        return np.array([weight])

    # The cost for a vehicle to take a diversion to the target
    # @param int vehicle = index of vehicle
    # @param int target = index of target
    # @return float = cost of diversion
    def cost(self,vehicle,target):
        # veh->target
        veh2tar = self.travelTime(vehicle=vehicle,target=target,source=True)

        # target->dest
        tar2dest = self.travelTime(vehicle=vehicle,target=target,source=False)

        # veh->dest (Shortest Path)
        veh2dest = self.travelTimeVeh2Dest(vehicle)

        # The cost is (veh->target + target->source) - veh->source 
        cost = veh2tar + tar2dest - veh2dest
    
        return cost
    
    # Determines the travel time between the vehicles current position and the destination
    # @param int iveh = vehicle index
    # @return float = Distance from Veh to Destination
    def travelTimeVeh2Dest(self,iveh):
        
        try:
            veh = env.vehicles_active[iveh]
        except IndexError:
            print('distance.py::88 Catching Index Error: iveh=',iveh)
            veh = env.vehicles_active[len(env.vehicles_active)-1]
        
        weight = veh['weight remaining'] + nxops.lookup_weight(veh['current edge']['to'],veh['destination node']['id'])
        
        # Determine the path with dijkstra. This is the path that starts from the node which the vehicle is currently moving along.
        # ~ path = nxops.dijkstra(env.nx,veh['current edge']['to'],veh['destination node']['id'])
        
        # ~ # Add the distance to complete the current edge to the weight of the planned path.
        # ~ weight = veh['weight remaining'] + nxops.path_info(env.nx,path)[0]
        
        
        return np.array(weight)
