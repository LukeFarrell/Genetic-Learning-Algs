'''
Created on Jun 21, 2016

@author: Jake Shulman
'''
import csv
import FirstNodeSVR
import FirstNodeNN
import FirstNodeAB

import FirstNodeD
import FirstNodeDATA
import FirstNodeDATAAB

# import NewMultiNode
# import MultiAttaBoost
# import MultiNeuralNet
import FirstNodeDATAAB
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from numpy import average
from FactorExtractor import extract
import time
 

inputs={}
inputsF = {}

def getFactors(ticker, daysBackward):
    FactorDict = extract(ticker, daysBackward)

    return FactorDict


def getFirstNode(ticker,numRuns,daysForward,daysBackward):
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=500+daysBackward
        window = 100
        columnNumber=29
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = FirstNodeSVR.train(ticker,window,1,2,columnNumber,1,numDataPoints-window,daysForward,daysBackward,randL[0:int(len(randL)*.3)],True)
        predict.append(a[3])
        error.append(a[2])
        Pcorrect.append(a[5])
    Start = a[6]
    
    return Start, average(predict),average(predict)-Start, np.std(predict), average(error), average(Pcorrect)

def getFirstNodeNN(ticker,numRuns,daysForward,daysBackward):
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=500+daysBackward
        window = 100
        columnNumber=29
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = FirstNodeNN.train(ticker,window,1,2,columnNumber,1,numDataPoints-window,daysForward,daysBackward,randL[0:int(len(randL)*.3)],True)
        predict.append(a[3])
        error.append(a[2])
        Pcorrect.append(a[5])
    Start = a[6]
    
    return Start, average(predict),average(predict)-Start, np.std(predict), average(error), average(Pcorrect)

def getFirstNodeAB(ticker,numRuns,daysForward,daysBackward):
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=500+daysBackward
        window = 100
        columnNumber=29
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = FirstNodeAB.train(ticker,window,1,2,columnNumber,1,numDataPoints-window,daysForward,daysBackward,randL[0:int(len(randL)*.3)],True)
        predict.append(a[3])
        error.append(a[2])
        Pcorrect.append(a[5])
    Start = a[6]
    
    return Start, average(predict),average(predict)-Start, np.std(predict), average(error), average(Pcorrect)


def getFirstNodeD(ticker,numRuns,daysForward,daysBackward):
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=200+daysBackward
        window = 5
        columnNumber=29
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = FirstNodeD.train(ticker,window,1,2,columnNumber,1,numDataPoints-window,daysForward,daysBackward,randL[0:int(len(randL)*.3)],True)
        predict.append(a[2])
        error.append(a[3])
        Pcorrect.append(a[5])
    Start = a[6]
    
    return Start, average(predict), average(predict)-Start, np.std(predict), average(error), average(Pcorrect)

def getFirstNodeV(ticker,numRuns,points,daysForward,daysBackward):
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=points+daysBackward
        window = 2
        columnNumber=29
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = FirstNodeDATA.train(ticker,window,1,2,columnNumber,1,numDataPoints-window,daysForward,daysBackward,randL[0:int(len(randL)*.3)],True)
        predict.append(a[2])
        error.append(a[4])
        Pcorrect.append(a[3])
    Start = a[6]
    yBack = a[5]
    
    return Start, average(predict), average(predict)-Start, np.std(predict), average(error), average(Pcorrect), yBack

def getFirstNodeVAB(ticker,numRuns,points,daysForward,daysBackward):
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=points+daysBackward
        window = 2
        columnNumber=29
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = FirstNodeDATA.train(ticker,window,1,2,columnNumber,1,numDataPoints-window,daysForward,daysBackward,randL[0:int(len(randL)*.3)],True)
        predict.append(a[2])
        error.append(a[4])
        Pcorrect.append(a[3])
    Start = a[6]
    yBack = a[5]
    
    return Start, average(predict), average(predict)-Start, np.std(predict), average(error), average(Pcorrect), yBack


def getMultiNode(ticker,numRuns,daysForward,daysBackward):
    global Start
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=1200+daysBackward
        window = 100
        columnNumber= 30
        numNodes = window
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = NewMultiNode.Main(ticker,window,1,2,columnNumber,1,numDataPoints,daysForward,daysBackward,numNodes)
        predict.append(a[0])
        error.append(a[2])
        Pcorrect.append(a[1])
        Start = a[4]
    
    return Start, average(predict),average(predict)-Start, np.std(predict), average(error), average(Pcorrect)

def getMultiAttaBoost(ticker,numRuns,daysForward,daysBackward):
    global Start
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=1200+daysBackward
        window = 100
        columnNumber= 30
        numNodes = window
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = MultiAttaBoost.Main(ticker,window,1,2,columnNumber,1,numDataPoints,daysForward,daysBackward,numNodes)
        predict.append(a[0])
        error.append(a[2])
        Pcorrect.append(a[1])
        Start = a[4]
    
    return Start, average(predict),average(predict)-Start, np.std(predict), average(error), average(Pcorrect)

def getMultiNeuralNet(ticker,numRuns,daysForward,daysBackward):
    global Start
    predict = []
    error = []
    Pcorrect = []
    for z in range(1,numRuns):
        numDataPoints=1200+daysBackward
        window = 100
        columnNumber= 30
        numNodes = window
        randL = []
        for y in range(1,int(numDataPoints-window-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        a = MultiNeuralNet.Main(ticker,window,1,2,columnNumber,1,numDataPoints,daysForward,daysBackward,numNodes)
        predict.append(a[0])
        error.append(a[2])
        Pcorrect.append(a[1])
        Start = a[4]
    
    return Start, average(predict),average(predict)-Start, np.std(predict), average(error), average(Pcorrect)

def setInputs(ticker,numRuns,daysForward,daysBackward):
    
    inputs["FirstNode"]     = getFirstNode(ticker,numRuns,daysForward,daysBackward)
    inputs["FirstNodeD"]    = getFirstNodeD(ticker,numRuns,daysForward,daysBackward)
    inputs["FirstNodeV"]    = getFirstNodeV(ticker, numRuns,160+daysBackward,daysForward,daysBackward)
    inputs["FirstNodeNN"]     = getFirstNodeNN(ticker,numRuns,daysForward,daysBackward)
    inputs["FirstNodeAB"]    = getFirstNodeAB(ticker,numRuns,daysForward,daysBackward)
    inputs["FirstNodeVAB"]    = getFirstNodeVAB(ticker, numRuns,160+daysBackward,daysForward,daysBackward)
    # inputs["FactorDeltas"]  = getFactors(ticker, daysBackward)[0]
    # inputs["FactorValues"]  = getFactors(ticker, daysBackward)[1]
    # inputs["FactorPercents"]= getFactors(ticker, daysBackward)[2]
    # inputs["MultiNode"]     = getMultiNode(ticker,numRuns,daysForward,daysBackward)
    # inputs["MultiAttaBoost"]= getMultiAttaBoost(ticker,numRuns,daysForward,daysBackward)
    # inputs["MultiNeuralNet"]= getMultiNeuralNet(ticker,numRuns,daysForward,daysBackward)

    # x = getFactors(ticker, numRuns, daysForward, daysBackward)
    # inputs["Factors"] = x[0]s
    # FactorNames = x[1]
    
#    inputs["MultiNode"]=getMultiNode(ticker,numRuns,daysForward,daysBackward)
#    inputs["MultiProcessor"]=getMultiProcessor(daysBackward, numRuns)
    return inputs
    
def setInputsF(ticker,numRuns,daysForward,daysBackward):
    
    a = setInputs(ticker, numRuns, daysForward, daysBackward)
    # a = x[0]
    # FactorNames = x[1]
 
    inputsF["FN1"]=a["FirstNode"][2]
    inputsF["FN2"]=a["FirstNode"][3]
    inputsF["FN3"]=a["FirstNode"][4]
    inputsF["FN4"]=a["FirstNode"][5]
    inputsF["FN5"]=abs(a["FirstNode"][2])

    inputsF["FND1"]=a["FirstNodeD"][2]
    inputsF["FND2"]=a["FirstNodeD"][3]    
    inputsF["FND3"]=a["FirstNodeD"][4]    
    inputsF["FND4"]=a["FirstNodeD"][5]    
    inputsF["FND5"]=abs(a["FirstNodeD"][2])    

    inputsF["FNV1"]=a["FirstNodeV"][2]
    inputsF["FNV2"]=a["FirstNodeV"][3]
    inputsF["FNV3"]=a["FirstNodeV"][4]
    inputsF["FNV4"]=a["FirstNodeV"][5]
    inputsF["FNV5"]=abs(a["FirstNodeV"][2])

    inputsF["FNNN1"]=a["FirstNodeNN"][2]
    inputsF["FNNN2"]=a["FirstNodeNN"][3]
    inputsF["FNNN3"]=a["FirstNodeNN"][4]
    inputsF["FNNN4"]=a["FirstNodeNN"][5]
    inputsF["FNNN5"]=abs(a["FirstNodeNN"][2])

    inputsF["FNAB1"]=a["FirstNodeAB"][2]
    inputsF["FNAB2"]=a["FirstNodeAB"][3]    
    inputsF["FNAB3"]=a["FirstNodeAB"][4]    
    inputsF["FNAB4"]=a["FirstNodeAB"][5]    
    inputsF["FNAB5"]=abs(a["FirstNodeAB"][2])    

    inputsF["FNVAB1"]=a["FirstNodeVAB"][2]
    inputsF["FNVAB2"]=a["FirstNodeVAB"][3]
    inputsF["FNVAB3"]=a["FirstNodeVAB"][4]
    inputsF["FNVAB4"]=a["FirstNodeVAB"][5]
    inputsF["FNVAB5"]=abs(a["FirstNodeVAB"][2])

    # inputsF["MN1"]=a["MultiNode"][2]
    # inputsF["MN2"]=a["MultiNode"][3]
    # inputsF["MN3"]=a["MultiNode"][4]
    # inputsF["MN4"]=a["MultiNode"][5]
    # inputsF["MN5"]=abs(a["MultiNode"][2]) 

    # inputsF["MAB1"]=a["MultiAttaBoost"][2]
    # inputsF["MAB2"]=a["MultiAttaBoost"][3]
    # inputsF["MAB3"]=a["MultiAttaBoost"][4]
    # inputsF["MAB4"]=a["MultiAttaBoost"][5]
    # inputsF["MAB5"]=abs(a["MultiAttaBoost"][2]) 

    # inputsF["MNN1"]=a["MultiNeuralNet"][2]
    # inputsF["MNN2"]=a["MultiNeuralNet"][3]
    # inputsF["MNN3"]=a["MultiNeuralNet"][4]
    # inputsF["MNN4"]=a["MultiNeuralNet"][5]
    # inputsF["MNN5"]=abs(a["MultiNeuralNet"][2]) 

    # for factor in a["FactorValues"].keys():
    #     inputsF[factor+"Value"] = a["FactorValues"][factor]

    # for factor in a["FactorDeltas"].keys():
    #     inputsF[factor+"Delta"] = a["FactorDeltas"][factor]

    # for factor in a["FactorPercents"].keys():
    #     inputsF[factor+"Percent"] = a["FactorPercents"][factor]

    
    return inputs, inputsF


    
if __name__ == '__main__':
    startT = time.time()
    print setInputsF("LUVBBF3", 5,1,2)[1]
    endT = time.time()
    print endT - startT