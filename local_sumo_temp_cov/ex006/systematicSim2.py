#import packages 
import numpy as np 
import matplotlib.pyplot as plt
import scipy.spatial.distance as spd 
import scipy.stats as stats


#define class for distance function 
class distance: 
	#class used for arrival time and distance calculations
	vP = None 
	tP = None
	def __init__(self,vP,tP):
		self.vP = vP
		self.tP = tP 
	def travelTime(self,vehicle,target,source): #return the distance between ith source/destination and jth target. s indicates source or destination (assuming unit speed). Return the first half if source is True, and return the second half if source is False. 
		vehicle = int(vehicle)
		target = int(target)
		if source:
			return spd.pdist([self.vP[2*vehicle],self.tP[target]])
		else: 
			return spd.pdist([self.tP[target],self.vP[2*vehicle+1]])
			
			
	def cost(self,vehicle,target):#cost for vehicle to take the diversion to target
		vehicle = int(vehicle)
		target = int(target)
		d1 = self.travelTime(vehicle=vehicle,target=target,source=True) #calculate distance from source to target 
		d2 = self.travelTime(vehicle=vehicle,target=target,source=False) #calculate distance from target to destination 
		sp = spd.pdist([self.vP[2*vehicle], self.vP[2*vehicle+1]])
		c = d1+d2-sp#cost c
		return c


class nashAssigner:
	N = None #number of vehicles 
	M = None #number of targets 
	R = None #max reward per sample
	tau = None 
	dist = None #object of class used for arrival time and distance calculations
	vP = None 
	arrivalTime = None #dictionary that maintains sequence of vehicle numbers and their arrival times
	decisionTime = None 
	targets = None 
	utilities = None 
	
	def __init__(self,N,M,R,tau,dist=None,arrivalTime={},decisionTime=0): #initialize 
		self.N = N 
		self.M = M 
		self.R = R
		self.tau = tau 
		self.dist = dist 
		self.arrivalTime = arrivalTime
		self.decisionTime = decisionTime
		#initalize arrival times at all targets to empty sets
		for t in range(self.M): self.arrivalTime[t] = []
		self.targets = np.zeros(self.N,dtype='float') #initalize by assigning random targets 
		for i in range(self.N): #assign random targets as initialization
			t = np.random.randint(low=0,high=self.M) #random target 
			at = self.decisionTime + self.dist.travelTime(vehicle=i,target=t,source=True)
			self.arrivalTime[t].append((i,at))
			self.targets[i] = t
		#sort the arrival times at all targets 
		for t in self.arrivalTime:
			self.arrivalTime[t].sort(key=lambda x: x[1],reverse=True)
		self.utilities = np.zeros(N) 
			
	
	def getUtility(self,si,t): #returns utility of vehicle si to go to target t (dependent on state of other vehicles)
		at = self.decisionTime + self.dist.travelTime(vehicle=si,target=t,source=True)#calculate arrival time of si at t 
		#calculate reward according to previous arrival time at t
		try:
			pat = next(x[1] for x in self.arrivalTime[t] if x[1] < at) #get the previous arrival time at t
			reward = self.R*(1-np.e**(-(at-pat)/self.tau))
		except StopIteration:
			reward = self.R 
		cost = self.dist.cost(vehicle=si,target=t)#calculate cost 
		return reward - cost 
	
	
	def getBestTarget(self,si):
		u = np.zeros(self.M)#array to store utilities 
		for t in range(self.M):#for each target 
			u[t] = self.getUtility(si,t)#calculate utility 
		return np.argmax(u)#return best target 
		
	
	def pair(self,si,t): #pair vehicle si with target t 
		tc = self.targets[si] #current target
		if tc == t: return #move along, nothing to do here
		#remove si and its arrival time from current target 
		sip = next(x for x in self.arrivalTime[tc] if x[0] == si) #vehicle, arrival time pair 
		self.arrivalTime[tc].remove(sip)
		#add si and its arrival time at the new target 
		at = self.decisionTime + self.dist.travelTime(vehicle=si,target=t,source=True)
		self.arrivalTime[t].append((si,at))
		self.arrivalTime[t].sort(key = lambda x: x[1], reverse=True)
		#assign the new target 
		self.targets[si] = t 
		
	def detach(self,si): #detaches the vehicle si from its current target 
		tc = self.targets[si] 
		if tc == np.nan: return 
		sip = next(x for x in self.arrivalTime[tc] if x[0] == si) #vehicle, arrival time pair 
		self.arrivalTime[tc].remove(sip)
		self.targets[si] = np.nan 


	
	def successor(self,si,t): #get the vehicle arriving after si at target t
		at = self.decisionTime + self.dist.travelTime(vehicle=si,target=t,source=True)
		try: 
			succ = next(x[0] for x in reversed(self.arrivalTime[t]) if x[1] > at)
		except StopIteration:
			succ = None 
		return succ 

	
	def closestTargetTo(self,si):
		distances = np.zeros(self.M) 
		for t in range(self.M):
			distances[t] = self.dist.travelTime(vehicle=si,target=t,source=True)
		return np.argmin(distances)	
	
	
	
	#function takes in a given configuration and returns target assignments 
	def getAssignments(self,max_iter=25): 
		#Returns: (targets, utilities)
		#targets[x] is the target allocation for vehicle x. If no target is assigned to x, then targets[x] will be equal to np.nan		
		#utilities[x] contains the utility of the vehicle x 
		count = self.N 
		iteration = 0
		while count:
			count = 0
			iteration = iteration + 1 
			if iteration > max_iter: 
				print('looks like an infinite loop, breaking')
				break 
			print('running iteration # %d'%iteration)
			S = set(range(self.N))	
			while S: 
				si = S.pop() #pick random vehicle 
				t1 = self.targets[si]
				tk = self.getBestTarget(si)#  arg max_l u(si,tl)
				if t1 != tk: 
					count += 1
					self.pair(si,tk) 
					sj = self.successor(si,tk)
					if sj: S.add(sj) 
		#calculate utilities at the Nash equilibrium
		for s in range(self.N):
			self.utilities[s] = self.getUtility(s,self.targets[s])
			if self.utilities[s] < 0: 
				self.detach(s)
		return (self.targets, self.utilities)
			
	
	def greedyAssignments(self): 
		#Returns: (targets, utilities)
		S = set(range(self.N))
		while S:
			si = S.pop()
			ti = self.closestTargetTo(si) 
			self.pair(si,ti) 
		for s in range(self.N):
			self.utilities[s] = self.getUtility(s,self.targets[s])
			if self.utilities[s] < 0: 
				self.targets[s] = np.nan 
		return (self.targets, self.utilities)
		
	def getTargetUtility(self,t):
		if not self.arrivalTime[t]: return 0 
		ats = [p[1][0] for p in self.arrivalTime[t]]
		ot = ats[0] + np.mean(ats) #end of observation period 
		ats = [ot] + ats 
		ats.append(self.decisionTime)
		ats = np.array(ats)
		its = ats[:-1] - ats[1:] #time intervals 
		its = its/np.sum(its) #normalize to make probabilities
		return stats.entropy(its,base=2)#/np.log2(len(its))
		
		
		
		
def getTargetAssignments(nA): 		
	print('final target allocation: (vehicle,target,utility)')
	allocations = []
	for x in range(nA.N):
		allocations.append('(%d,%.0f,%.3f)'%(x,nA.targets[x],nA.utilities[x]))
	return allocations
		

def getArrivalTimes(nA):
	print('arrival times at targets')
	arrivalTimes = []
	for x in nA.arrivalTime:
		times = ['(%d,%.2f)'%(p[0],p[1][0]) for p in nA.arrivalTime[x]] 
		arrivalTimes.append(times)
	return arrivalTimes


def getTargetUtilities(nA):
	targetUtilities = []
	for t in range(nA.M):
		targetUtilities.append(nA.getTargetUtility(t))
	return targetUtilities
	


def getRandomPlacement(N,M):
	vP = np.random.random((2*N,2))#sources and destinations
	tP = np.random.random((M,2))# targets 
	return (vP,tP)
	
	
def getLocalizedPlacement(N,M):
	vP = np.zeros(shape=(2*N,2))
	for i in range(N):
		a = np.random.random((2,2))
		vP[2*i:2*i+2,:] = (1/(1.2*(np.sum(a))))* a 
		vP[2*i+1,:] = 1-vP[2*i+1,:]
		
		
	
	
	r = np.random.random(M)-0.5 #random radii in [-0.5,0.5]
	theta = np.pi/2 + (np.pi/6)*np.random.random(M) #random ange in [pi/2-pi/6, pi/2+pi/6] 
	complexCrd = r*np.e**(1j*theta) 
	tP = np.zeros(shape=(M,2))
	tP[:,0] = np.real(complexCrd)
	tP[:,1] = np.imag(complexCrd)
	tP = (0.5,0.5) + tP 
	
	
	
	return (vP,tP)

def main():
	N = 100
	M = 20
	# vP,tP = getRandomPlacement(N,M)
	vP,tP = getLocalizedPlacement(N,M)
	dist = distance(vP,tP)#initialize distance object  
	
	#R should be in the upper range of the diversion costs 
	print('running smart assignment')
	nA = nashAssigner(N=N,M=M,R=5,tau=1,dist=dist) #initialize nash equilibrium algorithm
	nA.getAssignments()#get target assignments 
	smartUtilities = np.array(getTargetUtilities(nA))
	
	print('running greedy  assignment')
	nA.__init__(N=N,M=M,R=5,tau=1,dist=dist)
	nA.greedyAssignments()
	greedyUtilities =  np.array(getTargetUtilities(nA))
	
	plt.scatter(greedyUtilities,smartUtilities)
	m = np.maximum(greedyUtilities.max(), smartUtilities.max())+1
	plt.plot([0,m], [0,m], 'r')
	plt.xlabel('utitlities with greedy assignment')
	plt.ylabel('utilities with smart assignment')
	plt.show()
	
	
if __name__ == '__main__':
	main()















