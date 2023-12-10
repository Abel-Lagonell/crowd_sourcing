#import packages 
import numpy as np 
import matplotlib.pyplot as plt
import scipy.spatial.distance as spd 


#define class for distance function 
class distance: 
	vP = None 
	tP = None
	def __init__(self,vP,tP):
		self.vP = vP
		self.tP = tP 
	def travelTime(self,vehicle,target,source): #return the distance between ith source/destination and jth target. s indicates source or destination (assuming unit speed). Return the first half if source is True, and return the second half if source is False. 
		if source:
			return spd.pdist([self.vP[2*vehicle],self.tP[target]])
		else: 
			return spd.pdist([self.tP[target],self.vP[2*vehicle+1]])
	def cost(self,vehicle,target):#cost for vehicle to take the diversion to target
		d1 = self.travelTime(vehicle=vehicle,target=target,source=True) #calculate distance from source to target 
		d2 = self.travelTime(vehicle=vehicle,target=target,source=False) #calculate distance from target to destination 
		sp = spd.pdist([self.vP[2*vehicle], self.vP[2*vehicle+1]])
		c = d1+d2-sp#cost c
		return c


class nashAssigner:
	N = None #number of vehicles 
	M = None #number of targets 
	R = None 
	tau = None 
	dist = None
	arrivalTime = None 
	decisionTime = None 
	
	def __init__(self,N,M,R,tau,dist=None,arrivalTime={},decisionTime=0): #initialize 
		self.N = N 
		self.M = M 
		self.R = R
		self.tau = tau 
		self.dist = dist 
		self.arrivalTime = arrivalTime
		self.decisionTime = decisionTime


	#function takes in a given configuration and returns target assignments 
	def getAssignments(self): 
		#N: number of vehicles, M: number of targets, R: max reward per sample, dist: class used for arrival time and distance calculations, arrivalTime: dictionary that maintains sequence of vehicle numbers and their arrival times, decisionTime: The time at which the current assignment is being conducted. Is used to compute arrival time of vehicles at different targets.  
		#Returns: (cDest, utilities)
		#cDest[x] is the target allocation for vehicle x. If no target is assigned to x, then cDest[x] will be equal to np.nan		
		#utilities[x] contains the utility of the vehicle x 
		cDest = np.zeros(self.N,dtype='float') #initalize current destinations 
		for i in range(self.N): #assign random targets as initialization
			t = np.random.randint(low=0,high=self.M) #random target 
			at = self.decisionTime + self.dist.travelTime(vehicle=i,target=t,source=True)
			if t not in self.arrivalTime: 
				self.arrivalTime[t] = [(i,at)]
			else: 
				self.arrivalTime[t].append((i,at))
			cDest[i] = t
		for t in self.arrivalTime: #sorting arrival times at all targets in descending order 
			self.arrivalTime[t].sort(key = lambda x: x[1],reverse=True) 
		v = set(range(self.N)) #add all vehicles into a queue 
		while v:  #while queue is not empty 
			#find the best target location for the first vehicle 
			v1 = v.pop()
			#calculate utilities to all targets given current position of other vehicles 
			u = np.zeros(self.M)
			for t in range(self.M): 
				c = self.dist.cost(vehicle=v1,target=t)#cost 
				#calculate reward 
				if t not in self.arrivalTime: 
					r = self.R #full reward since no sample is taken at this location 
				else: 
					atv1 = self.decisionTime + self.dist.travelTime(vehicle=v1,target=t,source=True) #assuming unit speed 
					atOffsets = [x[1] for x in self.arrivalTime[t]] - atv1
					try:
						previousArrivalOffset = next(ato for ato in atOffsets if ato < 0) #get the offset to the previous sample 
						r = self.R*(1-np.e**(previousArrivalOffset/self.tau))
					except StopIteration: 
						r = self.R #v1 will be the first to arrive 
				u[t] = r-c #utility of reaching target t given the current destination of all other vehicles. 
			bestTarget = np.argmax(u)
			
			
			if bestTarget != cDest[v1]:#if the best target is not the current position 
				try: 
					v1Pair = next(x for x in self.arrivalTime[cDest[v1]] if x[0]==v1) #previous target should remove v1 from its list 
					self.arrivalTime[cDest[v1]].remove(v1Pair)
				except StopIteration: 
					print('could not find vehicle %d in its current destination %d'%(v1,cDest[v1]))
				cDest[v1] = bestTarget#move to the best target 
				d1 = self.dist.travelTime(vehicle=v1,target=t,source=True)
				#update arrival list att he target 
				atv1 = self.decisionTime + d1
				if bestTarget not in self.arrivalTime:
					self.arrivalTime[bestTarget] = [(v1,atv1)]
				else:
					self.arrivalTime[bestTarget].append((v1,atv1))
				self.arrivalTime[bestTarget].sort(key=lambda x: x[1],reverse=True)#sort the arrival time list in descending order 
				#add all vehicles arriving later than the current arrival into the queue 
				vArrivingLater = [x[0] for x in self.arrivalTime[bestTarget] if x[1] > atv1]
				for x in vArrivingLater: v.add(x)
		
		#calculate utitlies of all vehicles 
		utilities = np.zeros(self.N)
		rewards = np.zeros(self.N)
		costs = np.zeros(self.N)
		#calculate rewards and costs 
		for target in self.arrivalTime:#for each target 
			vehicles = [x for x in self.arrivalTime[target]]
			for i,vehicle in enumerate(vehicles):
				costs[vehicle[0]] = self.dist.cost(vehicle=vehicle[0],target=target)
				try:
					previousVehicle = vehicles[i+1]
					previousArrivalOffset = previousVehicle[1]-vehicle[1] #difference in arrival times (should be negative)
					rewards[vehicle[0]] = self.R*(1-np.e**(previousArrivalOffset/self.tau))
				except IndexError:
					rewards[vehicle[0]] = self.R #full reward for the first vehicle 
		#calculate utilities 
		utilities = rewards - costs
		
		for i,utililty in enumerate(utilities):
			if utililty < 0: cDest[i] = np.nan 
		
		return (cDest,utilities) #
	

def main():
	N = 50
	M = 25
	vP = np.random.random((2*N,2))#sources and destinations
	tP = np.random.random((M,2))# targets 
	dist = distance(vP,tP)#initialize distance instance 
	
	#R should be in the upper range of the diversion costs 
	
	nA = nashAssigner(N=N,M=M,R=5,tau=1,dist=dist) #initialize nash equilibrium algorithm
	t = nA.getAssignments()#get target assignments 
	cDest = t[0] 
	utilities = t[1]
	#print target assignments 
	print('final target allocation')
	for x in range(nA.N):
		print('vehicle,target,utililty: (%d,%.0f,%.3f)'%(x,cDest[x],utilities[x]))
	
	
if __name__ == '__main__':
	main()















