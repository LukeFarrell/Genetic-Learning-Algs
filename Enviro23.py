'''
Created on Jun 29, 2016

@author: Jake Shulman & Luke Farrell
'''
from Strategy import Strategy
from Portfolio import Portfolio 
from Species import Species
from Gene import Gene
import FirstNodeRunner as FNR
import random
import operator
import numpy as np
import matplotlib.pyplot as plt
from numpy import average
import IndividualTester
import csv as csv
import pickle
import multiprocessing as mp
import time

def MultiProcess1(portDict, Environment, startDay, DAYS, inputList, startPriceList, endPriceList, stockList, portfolio):
    for day in range(startDay, DAYS):
        inputs=inputList[day]  
        startPrice=startPriceList[day]
        endPrice=endPriceList[day]
        for gene in Environment.getPortfolios()[portfolio].getSpecies().getGenes().keys():
            Environment.getPortfolios()[portfolio].getSpecies().getGenes()[gene].makeBoolean(inputs)    
    # Get species output and add corresponding behavior
        # print Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice),Environment.getPortfolios()[portfolio].getShareFactor()
        Environment.getPortfolios()[portfolio].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() > Environment.getPortfolios()[portfolio].getSpecies().getRightThresh() , ("Buy", "LUV",int(Environment.getPortfolios()[portfolio].getShareFactor()*(Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice))),startPrice))
        Environment.getPortfolios()[portfolio].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() < Environment.getPortfolios()[portfolio].getSpecies().getLeftThresh(), ("Short", "LUV",int(Environment.getPortfolios()[portfolio].getShareFactor()*(Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice))),startPrice))
        Environment.getPortfolios()[portfolio].addGeneCorrect(endPrice-startPrice)
#Go through with actions, sellBack at end of day and add balance to balanceList
        Environment.getPortfolios()[portfolio].makeActions(startPrice)
        Environment.getPortfolios()[portfolio].sellBack(stockList,endPrice)
        Environment.getPortfolios()[portfolio].addBalance(Environment.getPortfolios()[portfolio].balance)  
    portDict[portfolio] =  Environment.getPortfolios()[portfolio]



def Enviro(stockList,Investment,numSpecies, genCount, shareCount, trainStart, trainEnd, testStart, testEnd, SaveNew, geneTest, evolutionPlot):
    avg=[]
    mx=[]
    graph={}
    g=[]
    TOPV=0
    TOP=0
    qg=[]
    
    Environment = Strategy(stockList)
    pInvest=Investment
    startDay = trainStart
    DAYS=trainEnd
    inputList={}
    startPriceList={}
    endPriceList={}
    
#Make Portfolios

    for individual in range(numSpecies):
        Environment.addPortfolio("p"+str(individual),pInvest)

#Set inputList
    try: 
        inputList = pickle.load( open( "inputListA.p", "rb" ) )
        startPriceList = pickle.load( open( "startPriceListA.p", "rb" ) )
        endPriceList = pickle.load( open( "endPriceListA.p", "rb" ) )
    except(IOError):
        print "Writing New Pickle"
    for d in range(startDay,DAYS):
        if d in inputList:
            pass
        else:
            print "Adding Day", d
            Environment.setInputs("LUVBBF3", d, d+1)
            inputList[d]=(Environment.getInputsF().copy())
            startPriceList[d]=Environment.getRecentPrice()
            endPriceList[d]=Environment.getEndPrice()
            pickle.dump( inputList, open( "inputListA.p", "wb" ) )
            pickle.dump( startPriceList, open( "startPriceListA.p", "wb" ) )
            pickle.dump( endPriceList, open( "endPriceListA.p", "wb" ) )

#Make lists for randomization of initial population

    inputs=inputList[startDay]
    variables=inputs.keys()
    right=[[],[]]
    weight=[]
    fitness={}
    delimeters=["<",">"]

 
    for valTop in np.arange(-1,1.1,.1):
        right[0].append(round(valTop,2))
    for y in variables:
        right[1].append(y)    
    for z in np.arange(0,1,.01):
        weight.append(round(z,3))
         
#Construct initial population

    for portfolio in Environment.getPortfolios().keys():
        p = Environment.getPortfolios()[portfolio]
        p.addSpecies(inputs)
        for variable in Environment.getPortfolios()[portfolio].getSpecies().getGenes().keys():
            a=random.randint(0,1)
            b=random.randint(0,len(right[a])-1)
            c=delimeters[random.randint(0,1)]
            d=weight[random.randint(0,99)]
            Environment.getPortfolios()[portfolio].getSpecies().addGene(variable,right[a][b],c,d)
        Environment.getPortfolios()[portfolio].getSpecies().setThresh(random.randrange(-len(Environment.getPortfolios()[portfolio].getSpecies().getGenes()),1)+0.0,random.randrange(0,len(Environment.getPortfolios()[portfolio].getSpecies().getGenes())+1)+0.0)
        Environment.getPortfolios()[portfolio].getSpecies().setShareFactor((random.randrange(1,100)))
# Start loop of days and generations     
    manager = mp.Manager()
    portDict = manager.dict()
    for gen in range(genCount):
        portDict.clear()
        t1 = time.time()

        print "Generation : ", gen+1
        pList = []
        for portfolio in Environment.getPortfolios().keys():
            proc = mp.Process(target = MultiProcess1, args = (portDict, Environment, startDay, DAYS, inputList, startPriceList, endPriceList, stockList, portfolio))
            pList.append(proc)
            proc.start()

        for proc in pList:
            if proc.is_alive():
                proc.join()
                
        for port in portDict.keys():
            Environment.getPortfolios()[port] = portDict[port]

#Get fitness of species
        for portfolio in Environment.getPortfolios().keys():
            #fitness[portfolio]=(Environment.getPortfolios()[portfolio].getCorrectList().count(1))*1.0/len(Environment.getPortfolios()[portfolio].getCorrectList())
            fitness[portfolio]=(Environment.getPortfolios()[portfolio].getCorrectList().count(1))*1.0/len(Environment.getPortfolios()[portfolio].getCorrectList())
            # Environment.getPortfolios()[portfolio].balanceList[-1]    
#Find top 50%

        sorted_fitness = sorted(fitness.items(), key=operator.itemgetter(1))
        if(sorted_fitness[-1][-1]>TOPV):
            TOP=sorted_fitness[-1][0]
            TOPV=sorted_fitness[-1][1]

#Get bottom 50%

        bottom=sorted_fitness[0:(numSpecies/2)]
     
#Choose 50 pairs of top 50
    
        top=sorted_fitness[numSpecies/2:numSpecies]
        topPair=[]
        # for valTop in range(len(top)):
        #     pair=valTop
        #     while top[pair][0]==top[valTop][0]:
        #         pair=random.randint(0,len(top)-1)
        #     topPair.append((top[valTop][0],top[pair][0]))
        pairs=[]
        for valTop in range(len(top)):
            for val2 in range(valTop+1,len(top)):
                pairs.append((top[valTop][0],top[val2][0]))
        np.random.shuffle(pairs)
        topPair=pairs[:numSpecies]

#For portfolio in 50 worst, set it equal to the breeding of a pair of top 50
    
        for valBot in range(len(bottom)):
            a = Environment.getPortfolios()[topPair[valBot][0]].getSpecies().copy()
            b=Environment.getPortfolios()[topPair[valBot][1]].getSpecies().copy()
            Environment.getPortfolios()[bottom[valBot][0]].resetAll(pInvest)
            Environment.getPortfolios()[bottom[valBot][0]].updateSpecies(a.breed(b).copy())

        q=[]
        for portfolio in range(len(Environment.getPortfolios().keys())):
            for port2 in range(portfolio+1,len(Environment.getPortfolios().keys())):
                if(portfolio!=port2):
                    q.append(Environment.getPortfolios()[Environment.getPortfolios().keys()[portfolio]].getSpecies().numEquals(Environment.getPortfolios()[Environment.getPortfolios().keys()[port2]].getSpecies()))
        print np.round(100.0*average(q)/len(Environment.getPortfolios()[Environment.getPortfolios().keys()[0]].getSpecies().getGenes()),2),"%"
        qg.append(100.0*average(q)/len(Environment.getPortfolios()[Environment.getPortfolios().keys()[0]].getSpecies().getGenes()))
        print np.round(time.time()-t1, 2), "seconds"
        print 
        print
        
        if(gen!=genCount-1):
            for valTop in range(len(top)):
                Environment.getPortfolios()[top[valTop][0]].reset(pInvest)
                                
    print TOPV, "Fitness"
    if(len(Environment.getPortfolios()[TOP].getCorrectList())==0):
        print "bad things happend there was nothing there, uh hello"
    else:
        print "TRAIN CORRECT   : ", (Environment.getPortfolios()[TOP].getCorrectList().count(1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
        print "TRAIN INCORRECT : ", (Environment.getPortfolios()[TOP].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
        print "TRAIN HELD      : ", (Environment.getPortfolios()[TOP].getCorrectList().count(0)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
        print "TRAIN GUESSED   : ", (Environment.getPortfolios()[TOP].getCorrectList().count(1)+Environment.getPortfolios()[TOP].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
    print "TRAIN BALANCE   : ", Environment.getPortfolios()[TOP].getBalanceList()[-1]

    pToO=[]

    for day in range(startDay,DAYS):
        inputs=inputList[day]  
        startPrice=startPriceList[day]
        endPrice=endPriceList[day] 
            
# Get boolean statements for the day   
        for gene in Environment.getPortfolios()[TOP].getSpecies().getGenes().keys():
            Environment.getPortfolios()[TOP].getSpecies().getGenes()[gene].makeBoolean(inputs)    
                    
# Get species output and add corresponding behavior
                # print Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice),Environment.getPortfolios()[portfolio].getShareFactor()
        Environment.getPortfolios()[TOP].addBehavior(Environment.getPortfolios()[TOP].getSpecies().getOutput() > Environment.getPortfolios()[TOP].getSpecies().getRightThresh() , ("Buy", "LUV",int(Environment.getPortfolios()[TOP].getShareFactor()*(Environment.getPortfolios()[TOP].getBalance()/(0.0+startPrice))),startPrice))
        Environment.getPortfolios()[TOP].addBehavior(Environment.getPortfolios()[TOP].getSpecies().getOutput() < Environment.getPortfolios()[TOP].getSpecies().getLeftThresh(), ("Short", "LUV",int(Environment.getPortfolios()[TOP].getShareFactor()*(Environment.getPortfolios()[TOP].getBalance()/(0.0+startPrice))),startPrice))
        Environment.getPortfolios()[TOP].addGeneCorrect(endPrice-startPrice)
#Go through with actions, sellBack at end of day and add balance to balanceList

        Environment.getPortfolios()[TOP].makeActions(startPrice)
        Environment.getPortfolios()[TOP].sellBack(stockList,endPrice)
        Environment.getPortfolios()[TOP].addBalance(Environment.getPortfolios()[TOP].balance)  
        pToO.append((Environment.getPortfolios()[TOP].getSpecies().getOutput(),(Environment.getPortfolios()[TOP].balanceList[-1]-Environment.getPortfolios()[TOP].balanceList[-2])/abs((Environment.getPortfolios()[TOP].balanceList[-1]-Environment.getPortfolios()[TOP].balanceList[-2]))))
    np.savetxt("pCorrectToOutput.csv", pToO, delimiter=",")

    # if evolutionPlot == True:
        # plt.plot(Environment.getPortfolios()[TOP].getBalanceList())
        # plt.show()

    if geneTest == True:
        for gene in Environment.getPortfolios()[TOP].getGeneCorrect():
            Environment.getPortfolios()[TOP].getGeneCorrect()[gene]=average(Environment.getPortfolios()[TOP].getGeneCorrect()[gene])
        # plt.bar(range(len(Environment.getPortfolios()[TOP].getGeneCorrect())), Environment.getPortfolios()[TOP].getGeneCorrect().values(), align='center')
        # plt.xticks(range(len(Environment.getPortfolios()[TOP].getGeneCorrect())), Environment.getPortfolios()[TOP].getGeneCorrect().keys())
        # plt.show()
        lsta=[]
        lstb=[]
        for gene in Environment.getPortfolios()[TOP].getGeneCorrect():
            lsta.append(Environment.getPortfolios()[TOP].getGeneCorrect()[gene])
            lstb.append(Environment.getPortfolios()[TOP].getSpecies().genes[gene].getWeight())
        # plt.plot(lsta,lstb,"go")
        print(np.corrcoef(lsta,lstb))
        # plt.show()
    #plt.plot(Environment.getPortfolios()[TOP].getShareCountList(),Environment.getPortfolios()[TOP].getOutputList(),"bo")
    # return IndividualTester.Test(Environment.getPortfolios()[TOP].getSpecies().getGenes(), testStart, testEnd, shareCount, Investment),(Environment.getPortfolios()[TOP].getCorrectList().count(1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
    return IndividualTester.Test(Environment.getPortfolios()[TOP], testStart, testEnd)
    # pCorrects=[]
    # for x in range(len(a)):
    #     pCorrects.append(sum(a[0:x+1])/float(x+1))
    # plt.plot(pCorrects)
    # plt.show()


if __name__ == '__main__':
    #stockList,Investment,numSpecies, genCount, shareCount, trainStart, trainEnd, testStart, testEnd, SaveNew, geneTest, evolutionPlot):
    #List of Stocks (As Strings)
    stockList = ["LUV"]
    #Principle Investment
    Investment = 10000
    #Number of Species 
    numSpecies = 1000
    #Number of Generation
    genCount = 100
    #Percent of Shares to trade each day
    shareCount = 0.8
    #Train Environment End Day (Last possible day)
    trainEnd = 400
    #Train Environment Start Day (Day Right before Testing)
    trainStart = 250
    #Test The winner on Environment End Day (less than Train)
    testEnd = 248
    #Test The winner on Environment Start Day (less than Train)
    testStart = 249
    #Write New CSV
    SaveNew = True
    #Test Gene percent Correct
    geneTest = True
    #Plot the evolution of the Top Species over all generations
    evolutionPlot = False

    # Enviro(stockList, Investment, numSpecies, genCount, shareCount, trainStart, trainEnd, testStart, testEnd, SaveNew, geneTest, evolutionPlot)
    cList=[]
    tList=[]
    bList=[]
    for x in range(245):
        #Call Enviro Function
        a=(Enviro(stockList, Investment, numSpecies, genCount, shareCount, trainStart, trainEnd, testStart, testEnd, SaveNew, geneTest, evolutionPlot))
        cList.append(a[0][0])
        tList.append(a[1])
        bList.append(a[0][1])
        testStart-=1
        testEnd-=1
        trainStart-=1
        SaveNew=False

    print(average(cList)),"TestingAverage"
    print(average(tList)),"TrainingAverage"


   
    np.savetxt("bList.csv", bList, delimiter=",")
    

