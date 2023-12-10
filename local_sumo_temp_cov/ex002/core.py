import env
import vehicle
import os
import pantherine as purr
import preprocess
import target
import nxops
import spm
import distance
import nash
import baseline

###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize(traci):
    os.system("cls")
    print("Initializing...")
    
    preprocess.initialize_nx()
    preprocess.initialize_edges_for_spawns_and_sinks(traci)
    target.initialize(traci)
    env.traci = traci
    vehicle.initialize()
    spm.generate_tar2dest()
    env.dist = distance.distance()
    
    n = 0; total = env.veh_exists_max;
    for i in range(0,env.veh_exists_max):
        vehicle.add()
        n += 1; purr.update(n,total,msg="Adding first %d vehicles " % (env.veh_exists_max))
        continue
        
    # ~ env.update_vehicle_info = True

    print("Initialization complete!")
    return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
# Return False to finalize the simulation
###############################
def timestep(traci,n_step):
    # Take samples if neccesary
    for vid in traci.vehicle.getIDList():
        if vehicle.is_veh_at_target(vid):
            vehicle.sample(vid,n_step)
    
    # We will wait until all vehicles spawn before assigning new routes. This may take 2-3 steps
    if env.first_update and (traci.vehicle.getIDCount() == env.veh_exists_max):
        env.first_update = False
        env.baseline_assign = True
        env.recalculate_nash = True
        env.update_vehicle_info = True
    
    # Update vehicle info if needed
    if (env.update_vehicle_info):
        vehicle.update()
        spm.update_veh2tar()
    
    # Set baseline assignments
    if env.method == 'baseline' and env.baseline_assign:
        env.baseline_assign = False
        baseline.assign()
    
    # Set Nash asignments
    if env.method == 'nash' and env.recalculate_nash:
        env.recalculate_nash = False
        nash.get_assignments()
    
    # End of Simulation condition
    if (traci.vehicle.getIDCount() <= 0) and (env.veh_id_counter >= (env.veh_total - 1)):
        print("All vehicles have arrived at their destinations.")
        return False
        
    # Add another vehicle condition
    elif traci.vehicle.getIDCount() < env.veh_exists_max and env.veh_id_counter < env.veh_total:
        print("\nAdding another vehicle.",env.veh_id_counter, env.veh_total)
        vehicle.add()
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
    target.csv()
    target.out_pretty()
    return
# End finalize
