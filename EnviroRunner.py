from Enviro23 import Enviro
import numpy as np
from numpy import average

#List of Stocks (As Strings)
stockList = ["LUV"]
#Principle Investment
Investment = 100000
#Number of Species 
numSpecies = 100
#Number of Generation
genCount = 150
#Percent of Shares to trade each day
shareCount = 0.8
#Train Environment End Day (Last possible day)
trainEnd = 400
#Train Environment Start Day (Day Right before Testing)
trainStart = 250
#Test The winner on Environment End Day (less than Train)
testEnd = 249
#Test The winner on Environment Start Day (less than Train)
testStart = 248
#Write New CSV
SaveNew = True
#Test Gene percent Correct
geneTest = True
#Plot the evolution of the Top Species over all generations
evolutionPlot = False

# Enviro(stockList, Investment, numSpecies, genCount, shareCount, trainStart, trainEnd, testStart, testEnd, SaveNew, geneTest, evolutionPlot)
cList=[]
tList=[]
bList=[Investment]
for x in range(245):
    print "PREDICTING FOR DAY : " , testStart
    np.savetxt("bList.csv", bList, delimiter=",")
    #Call Enviro Function
    a=(Enviro(stockList, Investment, numSpecies, genCount, shareCount, trainStart, trainEnd, testStart, testEnd, SaveNew, geneTest, evolutionPlot))
    cList.append(a[0])
    tList.append(a[1])
    bList.append(a[1])
    testStart-=1
    testEnd-=1
    trainStart-=1
    SaveNew=False
    print ""
    print "TEST AVERAGE  : ", (average(cList))
    print "TRAIN AVERAGE : ", (average(tList))
