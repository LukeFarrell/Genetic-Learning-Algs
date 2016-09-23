'''
Created on Apr 22, 2016

@author: Jake Shulman & Luke farrell
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import AdaBoostRegressor
from sklearn.preprocessing import StandardScaler
from numpy import average
import warnings
from mpl_toolkits.mplot3d import Axes3D

def train(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,end):
    
#   Gets data from file and converts to 2D array
    csv = np.genfromtxt (ticker+'.csv', delimiter=",")
    
#   Gets only columns and rows we want from array
    newCsv=csv[:,startCol:endCol][startRow:]
    
#   Finds number of columns being used
    numFactors=len(newCsv[0])
    
#   Creates array of 0's size we need
    X = [[0 for x in range(numFactors)] for y in range(numDataPoints)] 
    Xback = [[0 for x in range(numFactors)] for y in range(daysBackward)] 
#   Places values in array of deltas of -1st date to -1 - window days back, numDataPoints number of times
    for factor in range(0,numFactors):
        for day in range (0,numDataPoints):
            X[day][factor]= newCsv[-1-daysForward-day][factor]
        for day in range(0,daysBackward):
            Xback[day][factor]= newCsv[-1-daysForward-day][factor]
        
            

#   Makes target Vector
    y=csv[:,targetCol][len(csv)-numDataPoints:]
    yBack = csv[:,targetCol][-daysBackward:] 
    

#    print (Xback[0]) , len(Xback)
#    print (yBack[0]), len(yBack)    
#    print len(X) , "X"
##    print len(y),"y"
##    print len(randL),"randL"
#    for x in range(len(randL)):
#        print X[x]
    y=np.ndarray.tolist(y)


    dicty=[]
    for x in y:
        dicty.append(x)
#   Remove and set aside data points for testing
    testX=[]
    testY=[]
    for B in range(daysBackward):
        X.pop(len(X)-1)
        y.pop(len(y)-1)
    
    Ys = y
    for x in range(len(randL)):
        testX.append(X[randL[x]])
        testY.append(y[randL[x]])
        X[randL[x]]=10e36
        y[randL[x]]=10e36
    
    for x in range(len(randL)):
        X.remove(10e36)
        y.remove(10e36)
    
    y=y[::-1]   
    Ys = Ys[::-1]
    

    Start=0
    Y = []
    for day in range(len(y)):
        if day == 0:
            Start= y[day]
    
    Z = [[0 for l in range(numFactors)] for j in range(numDataPoints-daysBackward)] 
    for col in range(0,numFactors):
        for day in range (0,numDataPoints-daysBackward):
            Z[day][col]= newCsv[-1-day][col]-newCsv[-1-day][col]

    if end:
        Z = [[0 for l in range(numFactors)] for j in range(numDataPoints-daysBackward)] 
        for col in range(0,numFactors):
            for day in range (0,numDataPoints-daysBackward):
                Z[day][col]= newCsv[-daysForward-day][col]-newCsv[-daysForward-day][col]
        testX[-1] = Z[0]
            
        
    #Train model

    clf = AdaBoostRegressor(n_estimators = 100)

    X=np.asarray(X)
    y=np.asarray(y)
    
    
#   Test Model
    scaler = StandardScaler()
    scaler.fit(testX)
    scaler.fit(X)  

    X_train = scaler.transform(X)
    clf.fit(X_train, y)

    exper = []
    act = []
    testY = np.array(testY).reshape((len(testY), 1))
    warnings.filterwarnings("ignore", category=DeprecationWarning) 


    for x in testX:
        x = scaler.transform(x)  
        exper.append(clf.predict(x))
    for z in testY:
        act.append(z)
    
    
    predictions = []
    Xback= scaler.transform(Xback)
    predictions.append(clf.predict(Xback[0]))        
        
        
    errorGL = []
    percent = []
    for x in range(len(exper)):
        today = randL[x]
        todayG = exper[x]
        todayA = dicty[today]
        yesterday = dicty[today-1]
         
        errorG = abs(todayG - todayA)
        errorGL.append(errorG/todayA)
         
        dA= todayA - yesterday
        dG= todayG - yesterday
         
        if (dA < 0 and dG < 0) or (dA >0 and dG>0):
            percent.append(1)
        else:
            percent.append(0)
    
#     ERROR = []
#     for x in range(len(Xback)):
#         ERROR.append(abs((yBack[x] - predictions[x])/yBack[x]))
#     print average(ERROR) , "ERROR"
    
    
#     print average(percent)
    
#   Return Prediction     
#   return average(percent), average(errorGL)
#    print daysForward
#    print average(percent), average(errorGL)
    for x in range(len(exper)):
        exper[x]=exper[x][0]
    for x in range(len(act)):
        act[x]=act[x][0]
    
#     print average(percent), average(errorGL)
    return exper,act, predictions, average(percent), average(errorGL), yBack, Start,Ys

                                                       
if __name__ == '__main__':
    window = 10
    daysBackward= 45
    daysForward = 45
    predict = []
    error = []
    yBack =[]
    numDataPoints=140
    for x in range(daysBackward+daysForward+4,numDataPoints):
        randL = []
        for y in range(1,int(x-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)

        a = train("LUVBBF3",2,1,2,18,1,1000+x,1,daysBackward,randL[0:int(len(randL)*.35)],True)

        predict.append(a[2][0])
        print predict
        error.append(a[4])
    
    yBack.append(a[5])
    print yBack
    plt.plot(predict,"b--")
    plt.plot(yBack[0],"g-")

    plt.show()
    
    print average(error)
    
    print "done"
    

            
            
    