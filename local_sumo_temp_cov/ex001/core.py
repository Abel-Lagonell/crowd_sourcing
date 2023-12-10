import env
import vehicle
import os
import pantherine as purr
import preprocess
import target
from distance import distance
import nxops
import nash

###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize(traci):
    os.system("cls")
    print("Initializing...")
    
    preprocess.initialize_nx()
    preprocess.initialize_shortest_path_weights()
    preprocess.initialize_edges_for_spawns_and_sinks(traci)
    target.initialize(traci)
    
    n = 0; total = env.veh_exists_max;
    for i in range(0,env.veh_exists_max):
        vehicle.add(traci)
        n += 1; purr.update(n,total,msg="Adding first %d vehicles " % (env.veh_exists_max))
        continue
    
    if env.method == 'nash':
        env.dist = distance()
    
    print("Initialization complete!")
    return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
# Return False to finalize the simulation
###############################
def timestep(traci,n_step):
    env.traci = traci
    env.vids_active = traci.vehicle.getIDList()
    
    
    if env.method == 'nash':
        if env.recalculate_nash:
            nash.recalculate()
    
    # Check the position of each vehicle
    for vid in env.vids_active:
        if vehicle.is_veh_at_target(traci,vid):
            vehicle.sample(vid,n_step)
    
    # Simulation is ending
    if len(env.vids_active) == 0 and env.veh_id_counter >= env.veh_total:
        print("\nSimulation complete. Finalizing...")
        return False
        
    # Create more vehicles if neccesary
    elif len(env.vids_active) < env.veh_exists_max and env.veh_id_counter < env.veh_total:
        print("\nAdding vehicle %d/%d." % (env.veh_id_counter+1,env.veh_total))
        vehicle.add(traci)
    return True
# end timestep

###############################
# Finalize the Simulation
###############################
def finalize():
    if os.path.exists(env.out_dir):
        purr.deldir(env.out_dir)
    os.mkdir(env.out_dir)
    vehicle.csv()
    vehicle.out_pretty()
    target.json()
    target.out_pretty()
    return
# End finalize
