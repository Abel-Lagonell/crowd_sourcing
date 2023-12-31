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


#this class implements the nash assignment algorithm
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
	iterations = None 
	meanUtilities = None 
	changingVehicle = None #debug purpose only 
	
	def __init__(self,N,M,R,tau,dist=None,arrivalTime={},decisionTime=0): #initialize 
		self.N = N 
		self.M = M 
		self.R = 0 #start from 0 reward. ####to do### remove R from parameters 
		self.tau = tau 
		self.dist = dist 
		self.arrivalTime = arrivalTime
		self.decisionTime = decisionTime
		for t in range(self.M): self.arrivalTime[t] = [] #initalize arrival times at all targets to empty sets
		self.targets = np.empty(self.N) 
		self.targets[:] = np.nan #no targets assigned at the beginning because the reward is zero. 
		# self.targets = np.zeros(self.N,dtype='float') #initalize by assigning random targets 
		# for i in range(self.N): #assign random targets as initialization
			# t = np.random.randint(low=0,high=self.M) #random target 
			# at = self.decisionTime + self.dist.travelTime(vehicle=i,target=t,source=True)
			# self.arrivalTime[t].append((i,at))
			# self.targets[i] = t
		#sort the arrival times at all targets 
		# for t in self.arrivalTime:
			# self.arrivalTime[t].sort(key=lambda x: x[1],reverse=True)
		self.utilities = np.zeros(N)
		self.meanUtilities = [(0,0)] #will store reward value, average target utility pairs 
			
	
	def getUtility(self,si,t): #returns utility of vehicle si to go to target t (dependent on state of other vehicles)
		# at = self.decisionTime + self.dist.travelTime(vehicle=si,target=t,source=True)#calculate arrival time of si at t 
		# calculate reward according to previous arrival time at t
		# try:
			# pat = next(x[1] for x in self.arrivalTime[t] if x[1] < at) #get the previous arrival time at t
			# reward = self.R*(1-np.e**(-(at-pat)/self.tau))
		# except StopIteration:
			# reward = self.R 
		cost = self.dist.cost(vehicle=si,target=t)#calculate cost 
		reward = self.R*self.getRewardMultiplier(si,t)
		return reward - cost 
	
	
	def getBestTarget(self,si): #returns the target which provides best utility for vehicle si
		u = np.zeros(self.M)#array to store utilities 
		for t in range(self.M):#for each target 
			u[t] = self.getUtility(si,t)#calculate utility 
		return np.argmax(u)#return best target 
		
	
	def pair(self,si,t): #pair vehicle si with target t 
		tc = self.targets[si] #current target
		if tc == t: return #move along, nothing to do here
		#remove si and its arrival time from current target (if any) 
		if not np.isnan(tc):
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
	
	
	def getRewardMultiplier(self,si,t): #returns the reward multiplier for vehicle si at target t
		at = self.decisionTime + self.dist.travelTime(vehicle=si,target=t,source=True)#calculate arrival time of si at t	
		try:
			pat = next(x[1] for x in self.arrivalTime[t] if x[1] < at) #get the previous arrival time at t
			multiplier = 1-np.e**(-(at-pat)/self.tau)
		except StopIteration:
			multiplier = 1
		return multiplier
	
	def getNextChangePoint(self):
		changePoint = np.inf 
		for v in range(self.N): 
			if not np.isnan(self.targets[v]):
				for t in range(self.M):
					if t == self.targets[v]: continue
					ci = self.dist.cost(vehicle=v,target=self.targets[v])
					cj = self.dist.cost(vehicle=v,target=t)
					di = self.getRewardMultiplier(v,self.targets[v])
					dj = self.getRewardMultiplier(v,t)
					if di == dj: continue #parallel lines, current assignment is good 
					r = (ci-cj)/(di-dj)
					if r < changePoint and r > self.R: 
						changePoint = r 
						self.changingVehicle - v 
			else: 
				for t in range(self.M):
					r = self.dist.cost(vehicle=v,target=t)
					if r < changePoint and r > self.R: 
						changePoint = r 
						self.changingVehicle = v
		return changePoint
					
					
					
				
	
	def getAssignments(self):
		self.R = 0 #just in case
		iterations = 0 #for debug only 
		while True: 
			# iterations += 1
			self.R = self.getNextChangePoint()+ 10**(-8)
			if self.R == np.inf: break 
			self.getAssignmentsOld()#determine nash equilibrium 
			# if iterations < 5: 
				# print('assignments after iteration: %d'%iterations)
				# print('changing vehicle: %d'%self.changingVehicle)
				# print('change point determined to be %f'%self.R)
				# for v in range(self.N): print('%.0f,%f'%(v,self.targets[v]))
			# else: quit()
			newUitlity = self.getMeanTargetUtility()
			self.meanUtilities.append((float(self.R), newUitlity))
			# if iterations > 50: break 
		t = list(zip(*self.meanUtilities))
		rewards = np.array(t[0])
		averageUtilities = np.array(t[1])
		averageNormalizedUtility = np.divide(averageUtilities, rewards)
		plt.plot(rewards, averageUtilities)
		plt.scatter(rewards, averageUtilities)
		plt.xlabel('reward')
		plt.ylabel('average target utilities')
		plt.show()
		quit()
			
	
	
	#function takes in a given configuration and returns target assignments 
	def getAssignmentsOld(self): 
		# Returns: (targets, utilities)
		# targets[x] is the target allocation for vehicle x. If no target is assigned to x, then targets[x] will be equal to np.nan		
		# utilities[x] contains the utility of the vehicle x 
		count = self.N 
		iteration = 0
		while count:
			count = 0
			iteration = iteration + 1 
			if iteration > 25: break 
			# print('running iteration # %d'%iteration)
			S = set(range(self.N))
			startingAssignment = np.copy(self.targets) #used to check for cycles in the algorithm 
			transitionSequence = [startingAssignment]
			while S: 
				si = S.pop() #pick random vehicle 
				# si = list(S)[np.random.randint(len(S))]
				# S.remove(si)
				t1 = self.targets[si]
				tk = self.getBestTarget(si)#  arg max_l u(si,tl)
				if t1 != tk: 
					count += 1
					self.pair(si,tk) 
					sj = self.successor(si,tk)
					# print(si,t1,tk,sj)
					if sj: S.add(sj) 
					transitionSequence.append(np.copy(self.targets))
			endingAssignment = np.copy(self.targets) 
			if np.sum(startingAssignment==endingAssignment)==self.N and count > 0: #detected a cycle
				print('detected a cycle')
				# for each transition, find the cost to go to the new location 
				edgeCosts = []
				for i in range(len(transitionSequence)-1):
					# find the vechile which is tranisition
					tVehicle, = np.where(transitionSequence[i]!=transitionSequence[i+1])  
					# find the new target 
					tTarget = transitionSequence[i+1][tVehicle]
					edgeCosts.append(self.dist.cost(vehicle=tVehicle,target=tTarget))
				self.R = max(edgeCosts)-0.01
				print('adusted reward to %f'%self.R)
			# print(self.targets)	
				
			
		self.iterations = iteration
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
		
	def getMeanTargetUtility(self):
		targetUtilities = []
		for t in range(self.M):
			targetUtilities.append(self.getTargetUtility(t))
		return np.mean(targetUtilities)
		
		
		
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

def originalMain():
	N = 100
	M = 20
	vP,tP = getRandomPlacement(N,M)
	vP,tP = getLocalizedPlacement(N,M)
	dist = distance(vP,tP)#initialize distance object  
	
	# R should be in the upper range of the diversion costs 
	print('running smart assignment')
	nA = nashAssigner(N=N,M=M,R=5,tau=1,dist=dist) #initialize nash equilibrium algorithm
	nA.getAssignments()#get target assignments 
	smartUtilities = np.array(getTargetUtilities(nA))
	
	print('running greedy  assignment')
	nA.__init__(N=N,M=M,R=5,tau=1,dist=dist)
	nA.greedyAssignments()
	greedyUtilities =  np.array(getTargetUtilities(nA))
	
	plt.figure()
	plt.plot(vP[:,0], vP[:,1], 'ro')
	plt.plot(tP[:,0], tP[:,1], 'bo')
	
	plt.figure()
	plt.scatter(greedyUtilities,smartUtilities)
	m = np.maximum(greedyUtilities.max(), smartUtilities.max())+1
	plt.plot([0,m], [0,m], 'r')
	plt.xlabel('utitlities with greedy assignment')
	plt.ylabel('utilities with smart assignment')
	plt.show()


def largeTargetRegimeTesting():
	N = 20
	Ms = range(49,50)
	
	nOfIterations = []
	for M in Ms:
		print('running smart assignment, M=%d, N=%d'%(M,N))
		vP,tP = getLocalizedPlacement(N,M)
		dist = distance(vP,tP)#initialize distance object
		nA = nashAssigner(N=N,M=M,R=5,tau=1,dist=dist) #initialize nash equilibrium algorithm
		nA.getAssignments()#get target assignments 
		if nA.iterations >= 25: 
			with open('example_M_%d_N_%d.csv'%(M,N), 'w') as out: 
				out.write('%d,%d\n'%(2*N,M))
				for x in vP: out.write('%f,%f\n'%(x[0],x[1]))
				for x in tP: out.write('%f,%f\n'%(x[0],x[1]))
				
		nOfIterations.append((M,nA.iterations))
	
	nOfIterations = np.array(nOfIterations)
	print(nA.meanUtilities)
	# plt.stem(nOfIterations[:,0], nOfIterations[:,1])
	# plt.xlabel('M')
	# plt.ylabel('number of iterations')
	# plt.title('N=%d'%N)
	# plt.show()
	

def largeVehicleRegimeTesting():
	Ns = range(20,100)
	M = 10
	
	nOfIterations = []
	targetUtilities = []
	for N in Ns:
		print('running smart assignment, M=%d, N=%d'%(M,N))
		vP,tP = getLocalizedPlacement(N,M)
		dist = distance(vP,tP)#initialize distance object
		nA = nashAssigner(N=N,M=M,R=5,tau=1,dist=dist) #initialize nash equilibrium algorithm
		nA.getAssignments()#get target assignments 
		nOfIterations.append(nA.iterations)
		targetUtilities.append(np.mean(getTargetUtilities(nA)))
		print(nA.iterations)
	
	with open('largeVehicleRegimeTesting_1.csv','w') as out: 
		for i,N in enumerate(Ns):
			out.write('%d,%d,%f\n'%(N,nOfIterations[i],targetUtilities[i]))


def printLargeVehicleRegimeTestingData():
	with open('largeVehicleRegimeTesting_1.csv','r') as inp:
		lines = inp.read().splitlines()
	Ns = []
	nOfIterations = []
	targetUtilities = []
	for line in lines: 
		tokens = line.split(',')
		Ns.append(int(tokens[0]))
		nOfIterations.append(int(tokens[1]))
		targetUtilities.append(float(tokens[2]))
		
	fig,axs = plt.subplots(2,1,sharex=True) 
	axs[0].plot(Ns,nOfIterations)
	axs[1].plot(Ns,targetUtilities)
	axs[1].set_xlabel('number of vehicles')
	axs[0].set_ylabel('number of iterations')
	axs[1].set_ylabel('average utility')
	axs[0].set_title('number of targets M=10')
	plt.show()


def exampleNonConvergence():
	#read the locations from the input file 
	with open('example_M_5_N_20.csv', 'r') as inp: 
		lines = inp.read().splitlines()
	tokens = lines[0].split(',')
	N = int(tokens[0])
	M = int(tokens[1])
	positions = [ x.split(',') 	for x in lines[1:] ]
	vP = np.array(positions[:N])
	tP = np.array(positions[N:])
	N = int(N/2)
	dist = distance(vP,tP)#initialize distance object
		
	#perform nash assignment 
	nA = nashAssigner(N=N,M=M,R=5,tau=1,dist=dist) #initialize nash equilibrium algorithm
	nA.getAssignments()
	
	
def main():
	# np.random.seed(0)
	#largeVehicleRegimeTesting()
	printLargeVehicleRegimeTestingData()
	
	
	
if __name__ == '__main__':
	main()















