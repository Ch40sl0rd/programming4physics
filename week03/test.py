import numpy as np
import matplotlib.pyplot as plt

def riemannSum(func, interval, color, nBars):
    x = np.linspace(interval[0],interval[1], 1000)
    step = int(np.floor(1000/nBars))
    xBar = x[::step] 
    fBar = func(xBar)
    print(x,step,xBar,fBar)
    plt.bar(xBar,fBar,(xBar[1]-xBar[0]))
    plt.plot(x,func(x))
    plt.show()



riemannSum(np.sin, [0,np.pi], "r", 5)
