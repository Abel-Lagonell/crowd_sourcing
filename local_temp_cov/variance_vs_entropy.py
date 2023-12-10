import numpy as np 
import matplotlib.pyplot as plt 
import scipy.stats as stats

N = 1000
variances = np.zeros(N)
entropies = np.zeros(N)
for i in range(N):
	#generate random probability distribution 
	p = np.random.rand(20)
	p = p/np.sum(p)

	#compute variance 
	variances[i] = np.var(p)

	#compute entropy 
	entropies[i] = stats.entropy(p,base=2)
	
plt.plot(variances, entropies, '.')
plt.xlabel('variance')
plt.ylabel('entropy') 
plt.show()