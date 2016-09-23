'''
Created on May 22, 2016

@author: Jake Shulman & Luke Farrell
'''
import matplotlib.pyplot as plt
import numpy as np
from sknn.mlp import Regressor, Layer
from sklearn.preprocessing import StandardScaler
from numpy import average
import FirstNode
import time
import multiprocessing as mp
from functools import partial


def Train_X(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL, numNodes):
    data = FirstNode.train(ticker,numNodes,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[0:int((len(randL)*.35))],False)[0]
    return data

def Train_X2(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL, numNodes):
    data = FirstNode.train(ticker,numNodes,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[int((len(randL)*.35)):int((len(randL)*.7))],False)[0]
    return data

def Test_X(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL, numNodes):
    data = FirstNode.train(ticker,numNodes,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[int((len(randL)*.7)):],True)[0]
    return data 

def Main(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,numNodes):
    trainY=[]
    yBack = []
    randL = []
    
    start_time = time.time()
    
    for x in range(1,int(numDataPoints-daysBackward-daysForward)):
        randL.append(x)
    np.random.shuffle(randL)
    print "Step 1 Complete"

    #TrainX Process
    pool = mp.Pool(100)
    partial_TrainX = partial(Train_X,ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL )
    trainX = pool.map(partial_TrainX, (Node for Node in range(1,numNodes)))
    pool.close()
    pool.join()

    print "Step 2 Complete"

    pool = mp.Pool(100)
    partial_TrainX2 = partial(Train_X2,ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL )
    v = pool.map(partial_TrainX2, (Node for Node in range(1,numNodes)))
    pool.close()
    pool.join()
    
    print "Step 3 Complete"

    pool = mp.Pool(100)
    partial_TestX = partial(Test_X,ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL )
    testX = pool.map(partial_TestX, (Node for Node in range(1,numNodes)))
    pool.close()
    pool.join()
    
    print "Step 4 Complete"

    a = FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)
    trainY.append(a[1])
    Start = a[6]

    print "Step 5 Complete"
    yBack.append(FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)[4])
    trainXF=[]
    for x in range(len(trainX)):
        trainXF.append(trainX[x]+v[x])

    print "Training..."

    trainRXF=zip(*trainXF[::-1])
    testRX = zip(*testX[::-1])
    
    trainYF=trainY[0][0:len(trainRXF)]
    testY=trainY[0][len(trainRXF):]

    NumIterations = 100
    Layers = [Layer(type = "Sigmoid", units = 50), Layer(type = "Sigmoid", units = 50), Layer(type ="Linear")]
    model = Regressor(
    layers= Layers,
    learning_rate=.05,
    n_iter=NumIterations)

    model.fit(np.array(trainRXF), np.array(trainYF))
    print "fit!"
    
    predictions=[]
    for x in testRX:
        predictions.append(model.predict(np.array([x])))
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
    return PREDICTION, PERCENT, ERROR, yBack, Start



if __name__ == '__main__':
    timeS = time.time()
    numDaysForward = 5
    predictions= []
    percent = []
    error = []
    yBack = []
    ERROR = []
    for w in range(1,numDaysForward+1):        
        ticker="LUVBBF3"
        window= 700
        startRow=1
        startCol=2
        endCol=30
        targetCol=1
        daysForward= w
        daysBackward=w
        numNodes=window
        numDataPoints=1700-window
        a = Main(ticker, window, startRow, startCol, endCol, targetCol, numDataPoints, daysForward,daysBackward, numNodes)
        predictions.append(a[0][0][0])
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


