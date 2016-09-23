'''
Created on May 23, 2016

@author: Jake Shulman
'''
import matplotlib.pyplot as plt
import numpy as np
from numpy import average
import MultiNode


ticker="LOWBB"
window=10
startRow=1
startCol=2
endCol=17
targetCol=1
numDataPoints=2200-window
daysForward=1
numNodes=window
bigNet=[]
bigError=[]
for x in range(1,1000):
    print x
    MultiNode.trainMulti(ticker, window, startRow, startCol, endCol, targetCol, numDataPoints, daysForward, numNodes)

# net=a[0]
# error=a[1]
# print net
# print min(net)
# print max(net)
# print average(net)
# print average(error)
plt.plot(bigNet)
plt.show()
print "done"