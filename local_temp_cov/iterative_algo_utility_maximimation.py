#import packages 
import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx
import scipy.spatial.distance as spd 



np.random.seed(8)

#generate random targets, sources and destinations 
N = 50 #number of vehicles 
M = 50 #number of targets 
vP = np.random.random((2*N,2)) #sources and destinations for vehicles 
tP = np.random.random((M,2)) 


#calculate lengths of shortest paths 
sp = np.zeros(shape=(N,))
for i in range(N): 
	sp[i] = spd.pdist(vP[[2*i,2*i+1],:])[0]





#show the locations of vehicles and targets 
# plt.plot(vP[0,0], vP[0,1], marker='o',color='blue')
# plt.plot(vP[1,0], vP[1,1], marker='o',color='red')
# plt.plot(vP[2,0], vP[2,1], marker='v',color='blue')
# plt.plot(vP[3,0], vP[3,1], marker='v',color='red')
# plt.plot(vP[4,0], vP[4,1], marker='<',color='blue')
# plt.plot(vP[5,0], vP[5,1], marker='<',color='red')
# plt.plot(tP[:,0], tP[:,1], 'x')



#set a high enough reward so that diversions will be desirable 
R = 5 #maximum cost is 2.828
tau = 1 #maximum travel time is 1.414 


decisionTime = 0 #decision is being made at time 0

#add all vehicles into a queue 
v = set(range(N))
arrivalTime = {} #dictionary keyed by target number. Contains pairs of vehicle number, arrival time, sorted in descending order of arrival times 

#assign random targets to begin 
cDest = np.zeros(N,dtype='int') #-1 means original destination for the vehicle 
for i in range(N): 
	t = np.random.randint(low=0,high=M) #random target 
	at = decisionTime + spd.pdist([vP[2*i],tP[t]])
	if t not in arrivalTime: 
		arrivalTime[t] = [(i,at)]
	else: 
		arrivalTime[t].append((i,at))
	cDest[i] = t

for t in arrivalTime:
	arrivalTime[t].sort(key = lambda x: x[1],reverse=True) 


print('initial target allocation')
for x in range(N):
	print('(%d,%d)'%(x,cDest[x]))
	# plt.plot([vP[2*x,0],tP[cDest[x],0]], [vP[2*x,1],tP[cDest[x],1]], color='r')
# plt.title('initial target allocation')
 
 
while v:  #while queue is not empty 
	#find the best target location for the first vehicle 
	v1 = v.pop()
	print('(current vehicle,queue length,current target): (%d,%d,%d)'%(v1,len(v),cDest[v1]))
	#calculate utilities to all targets given current position of other vehicles 
	u = np.zeros(M)
	for t in range(M): 
		#calculate cost 
		d1 = spd.pdist([vP[2*v1],tP[t]])#calculate distance from source to target 
		d2 = spd.pdist([tP[t],vP[2*v1+1]])#calculate distance from target to destination 
		c = d1+d2-sp[v1]#cost 
		#calculate reward 
		if t not in arrivalTime: 
			r = R #full reward since no sample is taken at this location 
		else: 
			atv1 = decisionTime + d1 #assuming unit speed 
			atOffsets = [x[1] for x in arrivalTime[t]] - atv1
			try:
				previousArrivalOffset = next(ato for ato in atOffsets if ato < 0) #get the offset to the previous sample 
				r = R*(1-np.e**(previousArrivalOffset/tau))
			except StopIteration: 
				r = R #v1 will be the first to arrive 
		u[t] = r-c #utility of reaching target t given the current destination of all other vehicles. 
	bestTarget = np.argmax(u)
	
	
	if bestTarget == cDest[v1]:
		print('vehicle %d settles at target %d'%(v1,cDest[v1]))
		continue 
	if bestTarget != cDest[v1]:#if the best target is not the current position 
		print('moving vehicle %d to new target %d'%(v1,bestTarget))
		try: 
			v1Pair = next(x for x in arrivalTime[cDest[v1]] if x[0]==v1) #previous target should remove v1 from its list 
			arrivalTime[cDest[v1]].remove(v1Pair)
		except StopIteration: 
			print('could not find vehicle %d in its current destination %d'%(v1,cDest[v1]))
		cDest[v1] = bestTarget#move to the best target 
		d1 = spd.pdist([vP[2*v1],tP[t]])
		#update arrival list att he target 
		atv1 = decisionTime + d1
		if bestTarget not in arrivalTime:
			arrivalTime[bestTarget] = [(v1,atv1)]
		else:
			arrivalTime[bestTarget].append((v1,atv1))
		arrivalTime[bestTarget].sort(key=lambda x: x[1],reverse=True)#sort the arrival time list in descending order 
		#add all vehicles arriving later than the current arrival into the queue 
		vArrivingLater = [x[0] for x in arrivalTime[bestTarget] if x[1] > atv1]
		for x in vArrivingLater:
			v.add(x)
		print('adding following vehicle to queue:'+','.join([str(x) for x in vArrivingLater]))
		


# plt.figure()
# plt.plot(vP[0,0], vP[0,1], marker='o',color='blue')
# plt.plot(vP[1,0], vP[1,1], marker='o',color='red')
# plt.plot(vP[2,0], vP[2,1], marker='v',color='blue')
# plt.plot(vP[3,0], vP[3,1], marker='v',color='red')
# plt.plot(vP[4,0], vP[4,1], marker='<',color='blue')
# plt.plot(vP[5,0], vP[5,1], marker='<',color='red')
# plt.plot(tP[:,0], tP[:,1], 'x')
	
print('final target allocation')
for x in range(N):
	print('(%d,%d)'%(x,cDest[x]))
	# plt.plot([vP[2*x,0],tP[cDest[x],0]], [vP[2*x,1],tP[cDest[x],1]], color='b')

# plt.title('final target allocation')

# plt.show()




