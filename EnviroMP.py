'''
Created on September 2, 2016

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
from functools import partial

def EnviroInitializer(stockList,Investment,numSpecies, genCount, shareCount, startDay, endDay, testStart, testEnd, SaveNew, geneTest, evolutionPlot, geneChange, oldStart,oldEnd):
    avg=[]
    mx=[]
    graph={}
    g=[]
    TOPV=0
    TOP=0
    
    Environment = Strategy(stockList)
    pInvest=Investment
    startDay = startDay
    DAYS=endDay
    inputList={}
    startPriceList={}
    endPriceList={}
    inputListW = {}
    startPriceListW = {}
    endPriceListW = {}
    
#Make Portfolios

    for individual in range(numSpecies):
        Environment.addPortfolio("p"+str(individual),pInvest)
#Set Womb Battle days and womb change
    try: 
        inputListW = pickle.load( open( "inputListW1.p", "rb" ) )
        startPriceListW = pickle.load( open( "startPriceListW1.p", "rb" ) )
        endPriceListW = pickle.load( open( "endPriceListW1.p", "rb" ) )
    except(IOError):
        print "Writing New Pickle"
    for d in range(oldStart,oldEnd):
        if d in inputListW:
            print "Old Day", d, "Ready"
        else:
            print "Adding Old Day", d
            Environment.setInputs("LUVBBF3", d, d+1)
            inputListW[d]=(Environment.getInputsF().copy())
            startPriceListW[d]=Environment.getRecentPrice()
            endPriceListW[d]=Environment.getEndPrice()
            pickle.dump( inputListW, open( "inputListW1.p", "wb" ) )
            pickle.dump( startPriceListW, open( "startPriceListW1.p", "wb" ) )
            pickle.dump( endPriceListW, open( "endPriceListW1.p", "wb" ) )
#Set inputList
    try: 
        inputList = pickle.load( open( "inputListF1.p", "rb" ) )
        startPriceList = pickle.load( open( "startPriceListF1.p", "rb" ) )
        endPriceList = pickle.load( open( "endPriceListF1.p", "rb" ) )
    except(IOError):
        print "Writing New Pickle"
    for d in range(startDay,DAYS):
        if d in inputList:
            print "Day", d, "Ready"
        else:
            print "Adding Day", d
            Environment.setInputs("LUVBBF3", d, d+1)
            inputList[d]=(Environment.getInputsF().copy())
            startPriceList[d]=Environment.getRecentPrice()
            endPriceList[d]=Environment.getEndPrice()
            pickle.dump( inputList, open( "inputListF1.p", "wb" ) )
            pickle.dump( startPriceList, open( "startPriceListF1.p", "wb" ) )
            pickle.dump( endPriceList, open( "endPriceListF1.p", "wb" ) )

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
    
    return inputList, startPriceList, endPriceList, Environment

# Start loop of days and generations       

def DayRunner(inputList,startPriceList,endPriceList, gen, Environment, day):
    print "day " + str(day)  +" year "+ str(gen+1)
    inputs=inputList[day]  
    startPrice=startPriceList[day]
    endPrice=endPriceList[day] 
    
# Get boolean statements for the day   

    for portfolio in Environment.getPortfolios().keys():
        for gene in Environment.getPortfolios()[portfolio].getSpecies().getGenes().keys():
            Environment.getPortfolios()[portfolio].getSpecies().getGenes()[gene].makeBoolean(inputs)    
            
# Get species output and add corresponding behavior

    for portfolio in Environment.getPortfolios().keys():
        Environment.getPortfolios()[portfolio].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() > Environment.getPortfolios()[portfolio].getSpecies().getRightThresh() , ("Buy", "LUV",int(Environment.getPortfolios()[portfolio].getShareFactor()*(Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice))),startPrice))
        Environment.getPortfolios()[portfolio].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() < Environment.getPortfolios()[portfolio].getSpecies().getLeftThresh(), ("Short", "LUV",int(Environment.getPortfolios()[portfolio].getShareFactor()*(Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice))),startPrice))
        Environment.getPortfolios()[portfolio].addGeneCorrect(endPrice-startPrice)
#Go through with actions, sellBack at end of day and add balance to balanceList

    for portfolio in Environment.getPortfolios().keys():
        Environment.getPortfolios()[portfolio].makeActions(startPrice)
        Environment.getPortfolios()[portfolio].sellBack(stockList,endPrice)
        Environment.getPortfolios()[portfolio].addBalance(Environment.getPortfolios()[portfolio].balance)  
    

def GenRunner(inputList, startPriceList, endPriceList, startDay, endDay, gen, Environment, numSpecies, pInvest):
    fitness={}
    avg=[]
    mx=[]
    graph={}
    g=[]
    TOPV=0
    TOP=0

    partialDayRunner = partial(DayRunner, inputList, startPriceList, endPriceList, gen, Environment)
    Pool = mp.Pool(processes = 100)
    Pool.map(partialDayRunner, (day for day in range(startDay, endDay)))
    Pool.close()
    Pool.join()

    # for day in range(startDay, endDay):
    #     DayRunner(inputList,startPriceList,endPriceList,day, Environment)
#Get fitness of species
    for portfolio in Environment.getPortfolios().keys():
        # fitness[portfolio]=Environment.getPortfolios()[portfolio].balanceList[-1]
        fitness[portfolio]=(Environment.getPortfolios()[portfolio].getCorrectList().count(1))*1.0/len(Environment.getPortfolios()[portfolio].getCorrectList())    
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
    for valTop in range(len(top)):
        pair=valTop
        while top[pair][0]==top[valTop][0]:
            pair=random.randint(0,len(top)-1)
        topPair.append((top[valTop][0],top[pair][0]))
#For portfolio in 50 worst, set it equal to the breeding of a pair of top 50
    for valBot in range(len(bottom)):
        a = Environment.getPortfolios()[topPair[valBot][0]].getSpecies().copy()
        b=Environment.getPortfolios()[topPair[valBot][1]].getSpecies().copy()
        Environment.getPortfolios()[bottom[valBot][0]].resetAll(pInvest)
        Environment.getPortfolios()[bottom[valBot][0]].updateSpecies(a.breed(b).copy())
    for valTop in range(len(top)):
        Environment.getPortfolios()[top[valTop][0]].reset(pInvest)

    plt.plot(Environment.getPortfolios()[TOP].getBalanceList())

        # if geneChange == True:
        #     lsta=[]
        #     lstb=[]
        #     for gene in Environment.getPortfolios()[TOP].getGeneCorrect():
        #         lsta.append(average(Environment.getPortfolios()[TOP].getGeneCorrect()[gene]))
        #         lstb.append(Environment.getPortfolios()[TOP].getSpecies().genes[gene].getWeight())
        #     print(np.corrcoef(lsta,lstb)[0][1])
        #     Corro.append(np.corrcoef(lsta,lstb)[0][1])

def MainTester(stockList,Investment,numSpecies, genCount, shareCount, startDay, endDay, testStart, testEnd, SaveNew, geneTest, evolutionPlot, geneChange, oldStart,oldEnd):              
    
    print TOPV, "Fitness"
    print "SPECIES     : ", Environment.getPortfolios()[TOP].getSpecies().printSpecies()
    if len(Environment.getPortfolios()[TOP].getCorrectList()) == 0:
        print "IT HAPPENED"
    else:
        print "CORRECT     : ", (Environment.getPortfolios()[TOP].getCorrectList().count(1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
        print "INCORRECT   : ", (Environment.getPortfolios()[TOP].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
        print "HELD        : " , (Environment.getPortfolios()[TOP].getCorrectList().count(0)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
        print "GUESSED     : " , (Environment.getPortfolios()[TOP].getCorrectList().count(1)+Environment.getPortfolios()[TOP].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList())
    print "BALANCE     : ", Environment.getPortfolios()[TOP].getBalanceList()[-2]


    plt.show()

    if geneChange == True:
        plt.plot(range(genCount), Corro, 'go')
        plt.show()

    if evolutionPlot == True:
        plt.plot(Environment.getPortfolios()[TOP].getBalanceList())
        plt.show()

    if geneTest == True:
        for gene in Environment.getPortfolios()[TOP].getGeneCorrect():
            Environment.getPortfolios()[TOP].getGeneCorrect()[gene]=average(Environment.getPortfolios()[TOP].getGeneCorrect()[gene])
        plt.bar(range(len(Environment.getPortfolios()[TOP].getGeneCorrect())), Environment.getPortfolios()[TOP].getGeneCorrect().values(), align='center')
        plt.xticks(range(len(Environment.getPortfolios()[TOP].getGeneCorrect())), Environment.getPortfolios()[TOP].getGeneCorrect().keys())
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=90)
        plt.show()
        lsta=[]
        lstb=[]
        for gene in Environment.getPortfolios()[TOP].getGeneCorrect():
            lsta.append(Environment.getPortfolios()[TOP].getGeneCorrect()[gene])
            lstb.append(Environment.getPortfolios()[TOP].getSpecies().genes[gene].getWeight())
        print "CORRELATION :", np.corrcoef(lsta,lstb)[0][1]
        plt.plot(lsta,lstb,"go")
        plt.show()

    print "Testing Robustness..."
    IndividualTester.Test(Environment.getPortfolios()[TOP].getSpecies().getGenes(), testStart, testEnd, shareCount, Investment, SaveNewTest)


 
def main(stockList,Investment,numSpecies, genCount, shareCount, startDay, endDay, testStart, testEnd, SaveNew, geneTest, evolutionPlot, geneChange, oldStart,oldEnd):
    a = EnviroInitializer(stockList,Investment,numSpecies, genCount, shareCount, startDay, endDay, testStart, testEnd, SaveNew, geneTest, evolutionPlot, geneChange, oldStart,oldEnd)
    inputList = a[0]
    startPriceList = a[1]
    endPriceList = a[2]
    Environment = a[3]
    for gen in range(genCount):
        GenRunner(inputList, startPriceList, endPriceList, startDay, endDay, gen, Environment, numSpecies, Investment)


if __name__ == '__main__':
    #List of Stocks (As Strings)
    stockList = ["LUV"]
    #Principle Investment
    Investment = 10000
    #Number of Species 
    numSpecies = 1000
    #Number of Generation
    genCount = 4
    #Percent of Shares to trade each day
    shareCount = 0.9
    #
    oldEnd = 310
    #
    oldStart = 300
    #Train Environment End Day (Last possible day)
    endDay = 200
    #Train Environment Start Day (Day Right before Testing)
    startDay = 100
    #Test The winner on Environment End Day (less than Train)
    testEnd = 99
    #Test The winner on Environment Start Day (less than Train)
    testStart = 2
    #Write New CSV for Training
    SaveNew = False
    #Write New CSV for Testing 
    SaveNewTest = True
    #Test Gene percent Correct
    geneTest = True
    #Plot the evolution of the Top Species over all generations
    evolutionPlot = True
    #Plot how the gene correlation is changing over time
    geneChange = False
    #Call Enviro Function
    main(stockList, Investment,numSpecies, genCount, shareCount, startDay, endDay, testStart, testEnd, SaveNew, geneTest, evolutionPlot, geneChange, oldStart, oldEnd)
    
    

