'''
Created on May 22, 2016

@author: Jake Shulman & Luke Farrell
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from numpy import average
import FirstNode
import time


def trainMulti(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,numNodes):
    trainX=[]
    trainY=[]
    testX=[]
    yBack = []
#     error = []
    randL = []
    
    start_time = time.time()
    
    for x in range(1,int(numDataPoints-daysBackward-daysForward)):
        randL.append(x)
    np.random.shuffle(randL)
    print "Step 1"
    
    for x in range(1,numNodes):
        trainX.append(FirstNode.train(ticker,x,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[0:int((len(randL)*.35))],False)[0])
    print "Step 2"
    
    v=[] 
    for x in range(1,numNodes):
        v.append(FirstNode.train(ticker,x,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[int((len(randL)*.35)):int((len(randL)*.7))],False)[0])
        print "running.."
        
    print "Step 3"
    
    for x in range(1,numNodes):
        testX.append(FirstNode.train(ticker,x,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[int((len(randL)*.7)):],True)[0])
        print "running...."
        
    trainY.append(FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)[1])
    print "Step 4"
    yBack.append(FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)[4])
    trainXF=[]
    for x in range(len(trainX)):
        trainXF.append(trainX[x]+v[x])

    print "Training..."

    trainRXF=zip(*trainXF[::-1])
    testRX = zip(*testX[::-1])
    
    trainYF=trainY[0][0:len(trainRXF)]
    testY=trainY[0][len(trainRXF):]

    
    clf = svm.SVR(kernel="linear")

    clf.fit(trainRXF, trainYF)
    print "fit!"
    
    predictions=[]
    for x in testRX:
        predictions.append(clf.predict(x))
    error=[]
    
    for x in range(len(predictions)):
        error.append(abs(predictions[x]-testY[x])/testY[x])
    print average(error)
#    plt.plot(predictions,"g-")
#    plt.plot(testY,"b-")
#    plt.show()
    
    errorGL = []
    percent = []
    
    print predictions[-1]   
    randL.remove(len(randL))
    for x in range(len(predictions)):
        today = randL[x]
        todayG = predictions[x]
        todayA = trainY[0][today]
        yesterday = trainY[0][today-daysForward]
         
        errorG = abs(todayG - todayA)
        errorGL.append(errorG)
         
        dA= todayA - yesterday
        dG= todayG - yesterday
         
        if (dA < 0 and dG < 0) or (dA >0 and dG>0):
            percent.append(1)
        else:
            percent.append(0)
            

    print percent.count(1)/(len(percent)*1.0)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print "done"
    
    PREDICTION = predictions[-1]
    PERCENT = percent.count(1)/(len(percent)*1.0)
    ERROR = average(error)
    return PREDICTION, PERCENT, ERROR, yBack


    
        
    
#     print int(len(randL)*.35)
#     print int(len(randL)*.7)
#     print randL
#     print len(trainX)
#     print len(trainX[0])
#     print (trainY[0])
#     print len(trainY[0])
#     plt.plot(trainX[:,0],"g-")
#     plt.plot(trainY,"b-")


#     return , error



if __name__ == '__main__':
    timeS = time.time()
    numDaysForward = 10
    predictions= []
    percent = []
    error = []
    yBack = []
    ERROR = []
    for w in range(1,numDaysForward+1):        
        ticker="LUVBBF3"
        window= 100
        startRow=1
        startCol=2
        endCol=30
        targetCol=1
        daysForward= w
        daysBackward=w
        numNodes=window
        numDataPoints=1500-window
        a = trainMulti(ticker, window, startRow, startCol, endCol, targetCol, numDataPoints, daysForward,daysBackward, numNodes)
        predictions.append(a[0])
        percent.append(a[1])
        error.append(a[2])
    yBack.append(a[3])
    
    plt.plot(yBack[0][0],"g-")
    plt.plot(predictions, "b--")
    plt.show()
    
    timeFF = time.time()
    final_time = timeFF - timeS
    print "----------"+str(final_time)+"------------"
    print predictions
    print percent
    print error
    
    for x in range(len(predictions)):
        ERROR.append(yBack[0][0][x]-predictions[x]/abs(yBack[0][0][x]))
        
    print average(ERROR)
    plt.plot(ERROR, "r-")
    plt.show()
    
    plt.plot(percent,"b-")
    plt.show(2)
    plt.plot(error,"r-")
    plt.show(3)
    

    print "done"

    window = 100
    daysBackward=90
    daysForward = 90
    predict = []
    error = []
    yBack =[]
    for z in range(1,daysForward):
        randL = []
        for y in range(1,int(1000-window-daysBackward)):
            randL.append(y)
            np.random.shuffle(randL)
#
#        perc=[]
#   train("MMMBB",500,1,2,16,1,1700,1,randL[0:int(len(randL)*.3)],True)
        a = trainMulti("LUVBBF3",window,1,2,16,1,1000-window,z,daysBackward,randL[0:int(len(randL)*.3)],True)
##
        predict.append(a[3])
        print predict
        error.append(a[2])

    yBack.append(a[4])
    print yBack
    plt.plot(predict,"b--")
    plt.plot(yBack[0],"g-")

    plt.show()
    
    print average(error)
    
