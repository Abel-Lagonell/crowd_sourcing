#this script tests the use of a class as a function object with static data 

import numpy as np 
import scipy.spatial.distance as spd 

class exampleStatic: 
	vP = None 
	tP = None
	def __init__(self,vP,tP):
		self.vP = vP
		self.tP = tP 
	def dist(self,i,j): #return the distance between ith source and jth target 
		return spd.pdist([self.vP[2*i],self.tP[j]])
		
		
		
#generate random targets, sources and destinations 
N = 3 #number of vehicles 
M = 3 #number of targets 
vP = np.random.random((2*N,2)) #sources and destinations for vehicles 
tP = np.random.random((M,2)) 

exS = exampleStatic(vP,tP)

def functionUsingFunctionObject(dist, i,j):
	print('the distance is %f'%dist(i,j)) 
	
	
functionUsingFunctionObject(exS.dist,0,0); 






