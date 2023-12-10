# simSync.py
# Simulation Sychronizer

import pantherine as purr
import systematicSim2 as ss2
import math
import statistics
import os
import env

import numpy as np 
import matplotlib.pyplot as plt
import scipy.spatial.distance as spd 
import scipy.stats as stats

class SimulationSychronizer(object):
    nA_sumo_greedy = None
    nA_sumo_smart = None
    nA_geom_greedy = None
    nA_geom_smart = None
    out_dir_sumo = "sumo"
    out_dir_sumo_greedy = "greedy"
    out_dir_sumo_smart = "%smart"
    out_dir_geom = "geom"
    
    def __init__(self,map_dir,N,M,tau,R):
        self.map_dir = map_dir
        self.N = N
        self.M = M
        self.tau = tau
        self.R = R
        
        self.nodes = purr.readXMLtag(purr.mrf(self.map_dir,r'*.nod.xml'),'node')
        self.normalizeNodes(0.1)
        
        self.points_pybin = "temp/points.pybin"
        
        self.dst2src_point_validation()
        
        if not os.path.exists(self.out_dir_sumo):
            os.mkdir(self.out_dir_sumo)
        if not os.path.exists(self.out_dir_geom):
            os.mkdir(self.out_dir_geom)
        return
    
    # Selects N valid src->dst pairs from a set of 2*N
    def dst2src_point_validation(self):
        print("Determining valid src and destination points.")
        while True:
            # Determine vehicle start/dest and target SUMO nodes
            self.vP, self.tP = ss2.getLocalizedPlacement(2*self.N,self.M)
            vP_nodes = self.correlateNormalPoints2SumoNodes(self.vP,"Determining vehicle start/dest SUMO nodes ")
            self.vPs_nodes = []
            self.vPd_nodes = []
            for i, node in enumerate(vP_nodes):
                node['index'] = i
                if i % 2 == 0:
                    self.vPs_nodes.append(node)
                else:
                    self.vPd_nodes.append(node)
                continue
            del(vP_nodes)
            self.tP_nodes = self.correlateNormalPoints2SumoNodes(self.tP,"Correlating target SUMO nodes ")
            
            purr.save(self.points_pybin,(self.vPs_nodes,self.vPd_nodes,self.tP_nodes))
            
            # Run SUMO to validate points
            cmd = "python runner.py "
            cmd += "--nogui "
            cmd += "--map-dir=%s " % (self.map_dir)
            cmd += "--veh.total=%d " % (self.N)
            cmd += "--veh.exists.max=%d " % (self.N)
            cmd += "--method=%s " % ("validate.pts")
            cmd += "--points.file=%s " % (self.points_pybin)
            
            os.system(cmd)
            
            if purr.load(env.status_file):
                break
            continue
            
        self.vPs_nodes, self.vPd_nodes, self.tP_nodes = purr.load(env.valid_points_file)
        
        zipped_vP = []
        for i, node in enumerate(self.vPs_nodes):
            zipped_vP.append(node['index'])
            zipped_vP.append(self.vPd_nodes[i]['index'])
            
        temp = [self.vP[index] for index in zipped_vP]
        self.vP = temp
        
        print("Complete")
        
        return
        
    def run_sumo(self):
        purr.save(self.points_pybin,(self.vPs_nodes,self.vPd_nodes,self.tP_nodes))
        for method in ("greedy","smart"):
            cmd = "python runner.py "
            # ~ cmd += "--nogui "
            cmd += "--map-dir=%s " % (self.map_dir)
            cmd += "--veh.total=%d " % (self.N)
            cmd += "--veh.exists.max=%d " % (self.N)
            cmd += "--method=%s " % (method)
            cmd += "--points.file=%s " % (self.points_pybin)
            cmd += "--nash.R=%d " % (self.R)
            cmd += "--nash.tau=%f " % (self.tau)
            cmd += "--debug "
            if method == "greedy":
                cmd += "--out.dir=%s" % (self.out_dir_sumo_greedy)
            else:
                cmd += "--out.dir=%s" % (self.out_dir_sumo_smart)
            os.system(cmd)
            
            if method == "greedy":
                self.nA_sumo_greedy = purr.load(env.nA_greedy_file)
            else:
                self.nA_sumo_smart = purr.load(env.nA_smart_file)
            
            # ~ purr.pause()
            continue
        
    def run_geometric(self,max_iter=25):
        dist = ss2.distance(self.vP,self.tP)
        
        print('GEOMETRIC: running smart assignment')
        nA = ss2.nashAssigner(N=self.N,M=self.M,R=self.R,tau=self.tau,dist=dist) #initialize nash equilibrium algorithm
        nA.getAssignments(max_iter)#get target assignments 
        # ~ smartUtilities = np.array(ss2.getTargetUtilities(nA))
        
        self.nA_geom_smart = nA
        
        print('GEOMETRIC: running greedy  assignment')
        nA = ss2.nashAssigner(N=self.N,M=self.M,R=self.R,tau=self.tau,dist=dist)
        nA.greedyAssignments()
        # ~ greedyUtilities =  np.array(ss2.getTargetUtilities(nA))
        
        self.nA_geom_greedy = nA
        
        # ~ plt.scatter(greedyUtilities,smartUtilities)
        # ~ m = np.maximum(greedyUtilities.max(), smartUtilities.max())+1
        # ~ plt.plot([0,m], [0,m], 'r')
        # ~ plt.xlabel('utitlities with greedy assignment')
        # ~ plt.ylabel('utilities with smart assignment')
        # ~ plt.show()
        return
        
    def plot(self):
        # Geometric
        geom_smart_utilities = np.array(ss2.getTargetUtilities(self.nA_geom_smart))
        geom_greedy_utilities = np.array(ss2.getTargetUtilities(self.nA_geom_greedy))
        
        plt.figure(1)
        plt.scatter(geom_greedy_utilities, geom_smart_utilities)
        m = np.maximum(geom_greedy_utilities.max(), geom_smart_utilities.max()) + 1
        plt.plot([0,m],[0,m], 'r')
        plt.title("Geometric | N=%d M=%d R=%d tau=%.3f" % (self.N,self.M,self.R,self.tau))
        plt.xlabel('utitlities with greedy assignment')
        plt.ylabel('utilities with smart assignment')
        plt.savefig("%s/utility_N%dM%dR%dtau%.3f.png" % (self.out_dir_geom,self.N,self.M,self.R,self.tau))
        
        # SUMO
        sumo_smart_utilities = np.array(ss2.getTargetUtilities(self.nA_sumo_smart))
        sumo_greedy_utilities = np.array(ss2.getTargetUtilities(self.nA_sumo_greedy))
        
        plt.figure(2)
        plt.scatter(sumo_greedy_utilities, sumo_smart_utilities)
        m = np.maximum(sumo_greedy_utilities.max(), sumo_smart_utilities.max()) + 1
        plt.plot([0,m],[0,m], 'r')
        plt.title("SUMO | N=%d M=%d R=%d tau=%.3f" % (self.N,self.M,self.R,self.tau))
        plt.xlabel('utitlities with greedy assignment')
        plt.ylabel('utilities with smart assignment')
        plt.savefig("%s/utility_N%dM%dR%dftau%.3f.png" % (self.out_dir_sumo,self.N,self.M,self.R,self.tau))
        
        # Show
        plt.show()
        return
        
        
    
    # Correlates a set of points to nodes in a sumo MAP
    # @param P = Numpy array of normalized points
    # @param string msg = Message for progress bar
    # @return = A list of closest nodes (with error)
    def correlateNormalPoints2SumoNodes(self,P,msg=''):
        closestNode = [None for p in P]
        total = len(self.nodes) - 1
        for n,node in enumerate(self.nodes):
            nx = node['normX']
            ny = node['normY']
            for i,p in enumerate(P):
                px, py = p
                px = float(px)
                py = float(py)
                dist = math.sqrt(math.pow(nx-px,2) + math.pow(ny-py,2))
                if closestNode[i] == None or closestNode[i]['err'] > dist:
                    node['err'] = dist
                    closestNode[i] = node
                continue
            purr.update(n,total,msg)
            continue
        print()
        err = [node['err'] for node in closestNode]
        print("Mean err %.5f" % (statistics.mean(err))) 
        return closestNode
    
    # Adds two additional values to the node dictionaries:
    # normX and normY which are normalized X,Y values
    # @param float trim = % of border to trim [0,1]
    def normalizeNodes(self,trim):
        x = [float(node['x']) for node in self.nodes]
        y = [float(node['y']) for node in self.nodes]
        dx = max(x)-min(x)
        min_x = min(x) + dx*trim
        max_x = max(x) - dx*trim
        dy = max(y)-min(y)
        min_y = min(y) + dy*trim
        max_y = max(y) - dy*trim
        for i,node in enumerate(self.nodes):
            self.nodes[i]['normX'] = (float(node['x']) - min_x)/(max_x-min_x)
            self.nodes[i]['normY'] = (float(node['y']) - min_y)/(max_y-min_y)
            continue
        return
    pass

def run():
    map_dir = "../london-seg4/data/"
    N = 100 #100 # Vehicles
    M = 25 #25  # Targets
    tau = 1 
    R = 500   # Rewards
    
    ss = SimulationSychronizer(map_dir,N,M,tau,R)
    ss.run_sumo()
    ss.run_geometric()
    purr.save("temp/ss.pybin",ss)
    ss.plot()
    print("SUCCESS!")
    return

if __name__ == "__main__":
    run()
