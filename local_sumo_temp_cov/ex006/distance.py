# distance.py
# Author: Quentin Goss
import networkx as nx
import pantherine as purr
import env
import nxops
import networkx as nx
import numpy as np
import datetime as dtime
import spm

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
        iveh = int(vehicle); itar = int(target)
            
        # Retrieve Vehicle and Target Data
        veh = env.vehicles_active[iveh]
        tar = env.target_nodes[itar]
        
        if source:          
            weight = veh['weight remaining'] + spm.lookup(env.spm_veh2tar,tar['id'],veh['current edge']['to'])  
        else:
            weight = spm.lookup(env.spm_tar2dest,tar['id'],veh['destination node']['id'])
            
        return np.array([weight])

    # The cost for a vehicle to take a diversion to the target
    # @param int vehicle = index of vehicle
    # @param int target = index of target
    # @return float = cost of diversion
    def cost(self,vehicle,target):
        try:
            # veh->target
            veh2tar = self.travelTime(vehicle=vehicle,target=target,source=True)

            # target->dest
            tar2dest = self.travelTime(vehicle=vehicle,target=target,source=False)

            # veh->dest (Shortest Path)
            veh2dest = self.travelTimeVeh2Dest(vehicle)
        except nx.NetworkXNoPath:
            return np.array([np.inf])

        # The cost is (veh->target + target->source) - veh->source 
        cost = veh2tar + tar2dest - veh2dest
    
        return cost
    
    # Determines the travel time between the vehicles current position and the destination
    # @param int iveh = vehicle index
    # @return float = Distance from Veh to Destination
    def travelTimeVeh2Dest(self,iveh):
        veh = env.vehicles_active[iveh]
        return np.array(veh['veh2dest weight'])
