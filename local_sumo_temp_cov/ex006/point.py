# point.py
import env
import pantherine as purr
import vehicle
import networkx as nx
import sys

def validate():
    if not env.method == "validate.pts":
        return
    vPs = []
    vPd = []
    n = 0; total = env.veh_total
    for i in range(2*env.veh_total):
        try:
            vehicle.shortest_path(i)
            n += 1; purr.update(n,total,"Gathering valid points ")
            vPs.append(env.vPs[i])
            vPd.append(env.vPd[i])
            if len(vPs) == env.veh_total:
                print("\nValid points determined. Exiting...")
                purr.save(env.valid_points_file,(vPs,vPd,env.tP))
                purr.save(env.status_file,True)
                sys.exit(0)
        except nx.NetworkXNoPath:
            pass
        continue
    print("Not good points, need to reload.")
    purr.save(env.status_file,False)
    sys.exit(0)
    return
