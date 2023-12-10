import numpy as np 
import matplotlib.pyplot as plt 


a = np.arange(0,10,0.01)
R = 3 + np.arctan(a-5)

plt.plot(a,R)
plt.show()