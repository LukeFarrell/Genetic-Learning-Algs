'''
Created on Apr 22, 2016

@author: Jake Shulman & Luke farrell
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
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
    
#   Places values in array of deltas of -1st date to -1 - window days back numDataPoints number of times
    for factor in range(0,numFactors):
        for day in range (0,numDataPoints):
            X[day][factor]= newCsv[-1-daysForward-day][factor]-newCsv[-1-daysForward-day-window][factor]

#   Makes target Vector

    y=csv[:,targetCol][len(csv)-numDataPoints:]
    
    y=np.ndarray.tolist(y)
    dicty=[]
    for x in y:
        dicty.append(x)
#   Remove and set aside data points for testing
    testX=[]
    testY=[]
    xBack = []
    yBack = []
    for B in range(daysBackward):
        xBack.append(X.pop(len(X)-1))
        yBack.append(y.pop(len(y)-1))
    
    yBack = yBack[::-1]
    
    y=y[::-1]

    Start=0
    Y = []
    for day in range(len(y)):
        if day == 0:
            Start= y[day]
            Y.append(0)
        else:
            Y.append(y[day]-y[day-1])

    YBack = []
    for day in range(len(yBack)):
        if day == 0:
            YBack.append(0)
        else:
            YBack.append(yBack[day]-yBack[day-1])    
            
    for x in range(len(randL)):
        testX.append(X[randL[x]])
        testY.append(Y[randL[x]])
        X[randL[x]]=10e36
        Y[randL[x]]=10e36
        
    
    for x in range(len(randL)):
        X.remove(10e36)
        Y.remove(10e36)
    
    


    Z = [[0 for l in range(numFactors)] for j in range(numDataPoints)] 
    for col in range(0,numFactors):
        for day in range (0,numDataPoints):
            Z[day][col]= newCsv[-1-day][col]-newCsv[-1-day-window][col]

    if end:
        Z = [[0 for l in range(numFactors)] for j in range(numDataPoints)] 
        for col in range(0,numFactors):
            for day in range (0,numDataPoints):
                Z[day][col]= newCsv[-daysForward-day][col]-newCsv[-daysForward-day-window][col]
        testX[-1] = Z[0]
            
    #Train model

    clf = svm.SVR(kernel="rbf") #78

    X=np.asarray(X)
    y=np.asarray(Y)

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
    for y in testY:
        act.append(y)
        
    Error = []
    Xback = scaler.transform(xBack)
    predictions = (clf.predict(Xback[0]))
        
    predictionsF = Start+predictions
#     for x in range(len(predictions)):
#         Start =Start+ predictions[x]
#         predictionsF.append(Start)
        
    
#     for day in range(len(predictionsF)):
#         if day!= 0:
#             Error.append(abs((yBack[day]-predictionsF[day])/yBack[day]))
            

        
    errorGL = []
    percent = []
    for x in range(len(exper)):
        today = randL[x]
        yesterday = dicty[today-daysForward]
        todayG = exper[x]+yesterday
        todayA = dicty[today]

         
        errorG = abs(todayG - todayA)
        errorGL.append(errorG/todayA)
         
        dA= todayA - yesterday
        dG= todayG - yesterday
         
        if (dA < 0 and dG < 0) or (dA >0 and dG>0):
            percent.append(1)
        else:
            percent.append(0)
    
#     print average(percent)
    
#   Return Prediction     
#   return average(percent), average(errorGL)
#     print average(percent), average(errorGL)
    for x in range(len(exper)):
        exper[x]=exper[x][0]
    for x in range(len(act)):
        act[x]=act[x][0]
    
    
#    plt.plot(exper, "b--")
#    plt.plot(act,"g-")
#    plt.show()    
    
    return exper,act, predictionsF, average(errorGL), yBack, average(percent), Start

                                                       
if __name__ == '__main__':

    window = 5
    percentL = []
    Error = []
    daysBackward = 45
    ErrorF = []
    
    for w in range(1,20):
#        for z in range(3,factors):
        randL = []
        for y in range(1,int(200-w-daysBackward)):
            randL.append(y)
            np.random.shuffle(randL)
    #
    #        perc=[]
    #train(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,randL,end)
        a = train("LUVBBF3",5,1,2,23,1,200-w,1,daysBackward,randL[0:int(len(randL)*.3)],True)
         #   b = train("AAONBBF",z,1,2,10,1,2500-800,1,randL[0:int(len(randL)*.3)],True)        
        predictions = a[2]
        actual = a[3]
        exper = a[0]
        act = a[1]
    plt.plot(exper,"b--")

    Error.append(average(a[4]))
    plt.plot(act,"g-")

#        ErrorF.append(average(Error))
#    plt.plot(Error, "r-")
    plt.show()
    print average(Error)
#
#    plt.plot(ErrorF, "b-")
#    plt.show()

    plt.show()
    
    print "done"
    

            
            
    