# spm.py
# Author: Quentin
# Shortest Path Matrix methods
import nxops
import pantherine as purr
import env
import networkx as nx

# The distances between the targets and each destination may be determined after destination nodes are chosen
def generate_tar2dest():
    print("Generating Tar -> Dest shortest path weights...")
    tar_ids = [tar['id'] for tar in env.target_nodes]
    dest_ids = [veh['shortest path']['nids'][-1] for veh in env.vehicles]
    env.spm_tar2dest = generate(tar_ids,dest_ids)
    print("Complete")
    return

# Generates a shortest path matrics from two sets of node IDS
# @param [str] colnames: Node IDs of the columns
# @param [str] rownames: Node IDs of the rows
# @return a dictionary with the short path matrix
def generate(colnames,rownames):
    weights = []
    n = 0; total = len(colnames) * len(rownames)
    for irow,rn in enumerate(rownames):
        row = []
        for icol,cn in enumerate(colnames):
            weight = float('inf')
            if not cn == rn:
                weight = nxops.path_info(env.nx,nx.dijkstra_path(env.nx,cn,rn))[0]
            row.append(weight)
            n+=1;purr.update(n,total,"Generating SPM ")
            continue
        weights.append(row)
        continue
    spm = {
        'colnames':colnames,
        'rownames':rownames,
        'weights':weights
    }
    print()
    return spm

# Prints an SPM visually 
def display(spm):
    print('%11s' % (''), end='')
    [print('%10s ' % (cn[:10]),end='') for cn in spm['colnames']]
    print()
    for irow, row in enumerate(spm['weights']):
        print('%10s:' % (spm['rownames'][irow][:10]),end='')
        for i, val in enumerate(row):
            print('%10.3f ' % (val),end='')
            continue
        print()
        continue
    return

# Update the shortest Path Matrix for veh->tar
# The matrix should consist of every possible option:
#  - Next Node IDS for every Vehicle to Every Target
def update_veh2tar():
    veh_next_nids = [veh['current edge']['to']for veh in env.vehicles_active]
    tar_ids = [tar['id'] for tar in env.target_nodes]
    env.spm_veh2tar = generate(tar_ids,veh_next_nids)
    return

# Looks up a weight from an spm
# @param dict spm = Shortest Path Matrix
# @param str colname = Column name
# @param str rowname = Row name
def lookup(spm,colname,rowname):
    icol = spm['colnames'].index(colname)
    irow = spm['rownames'].index(rowname)
    if icol < 0 or irow < 0:
        raise IndexError
    return spm['weights'][irow][icol]
    
    
