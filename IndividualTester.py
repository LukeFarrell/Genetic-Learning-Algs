'''
Created on Jun 29, 2016

@author: Jake Shulman
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
import Enviro
import pickle

def Test(TopSpecies, testStart, testEnd, shareCount, Investment):
    for x in range(1):
        stockList=["LUV"]
        avg=[]
        mx=[]
        graph={}
        g=[]
        TOPV=0
        Graph = []
        
    
                
        Environment = Strategy(stockList)
        numSpecies=1
        pInvest=Investment
        genCount=1
        startDay= testStart
        DAYS= testEnd
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
                print "Day", d, "Ready"
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
             
    #Construct test population
        for portfolio in Environment.getPortfolios().keys():
            p = Environment.getPortfolios()[portfolio]
            p.addSpecies(inputs)
            
        for gene in TopSpecies:
            Environment.getPortfolios()['p0'].getSpecies().addGene(TopSpecies[gene].left,TopSpecies[gene].right, TopSpecies[gene].delimeter, TopSpecies[gene].weight)
                
    # Start loop of days and generations     
        
        for day in range(startDay, DAYS):
            print "day", day
            inputs=inputList[day]  
            startPrice=startPriceList[day]
            endPrice=endPriceList[day] 
            
# Get boolean statements for the day   
     
            for portfolio in Environment.getPortfolios().keys():
                for gene in Environment.getPortfolios()[portfolio].getSpecies().getGenes().keys():
                    Environment.getPortfolios()[portfolio].getSpecies().getGenes()[gene].makeBoolean(inputs)    
                    
# Get species output and add corresponding behavior

            Environment.getPortfolios()["p0"].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() > Environment.getPortfolios()[portfolio].getSpecies().getRightThresh() , ("Buy", "LUV",int(Environment.getPortfolios()[portfolio].getShareFactor()*(Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice))),startPrice))
            Environment.getPortfolios()["p0"].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() < Environment.getPortfolios()[portfolio].getSpecies().getLeftThresh(), ("Short", "LUV",int(Environment.getPortfolios()[portfolio].getShareFactor()*(Environment.getPortfolios()[portfolio].getBalance()/(0.0+startPrice))),startPrice))
            Environment.getPortfolios()["p0"].addGeneCorrect(endPrice-startPrice)
#Go through with actions, sellBack at end of day and add balance to balanceList

            Environment.getPortfolios()["p0"].makeActions(startPrice)
            Environment.getPortfolios()["p0"].sellBack(stockList,endPrice)
            Environment.getPortfolios()["p0"].addBalance(Environment.getPortfolios()[portfolio].balance)  

            # for gene in Environment.getPortfolios()["p0"].getGeneCorrect():
            #     Environment.getPortfolios()["p0"].getGeneCorrect()[gene]=average(Environment.getPortfolios()["p0"].getGeneCorrect()[gene])
            # plt.bar(range(len(Environment.getPortfolios()["p0"].getGeneCorrect())), Environment.getPortfolios()["p0"].getGeneCorrect().values(), align='center')
            # plt.xticks(range(len(Environment.getPortfolios()["p0"].getGeneCorrect())), Environment.getPortfolios()["p0"].getGeneCorrect().keys())
            # plt.show()
            # lsta=[]
            # lstb=[]
            # for gene in Environment.getPortfolios()["p0"].getGeneCorrect():
            #     lsta.append(Environment.getPortfolios()["p0"].getGeneCorrect()[gene])
            #     lstb.append(Environment.getPortfolios()["p0"].getSpecies().genes[gene].getWeight())
            # plt.plot(lsta,lstb,"go")
            # print(np.corrcoef(lsta,lstb))
            # plt.show()
    #Add balanceList to graph
        
        for portfolio in Environment.getPortfolios().keys():
            print Environment.getPortfolios()[portfolio].getBalanceList()

        for portfolio in Environment.getPortfolios().keys():
            fitness[portfolio]=Environment.getPortfolios()[portfolio].balanceList[-1]
                     
        sorted_fitness = sorted(fitness.items(), key=operator.itemgetter(1))
   
        if(sorted_fitness[-1][-1]>TOPV):
            TOP=sorted_fitness[-1][0]
            TOPV=sorted_fitness[-1][1]
                
        print "TEST DAY        : " , DAYS
        print "TEST CORRECT    : " , (Environment.getPortfolios()["p0"].getCorrectList().count(1)*1.0)/len(Environment.getPortfolios()["p0"].getCorrectList())
        print "TEST INCORRECT  : " , (Environment.getPortfolios()["p0"].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()["p0"].getCorrectList())
        print "TEST HELD       : " , (Environment.getPortfolios()["p0"].getCorrectList().count(0)*1.0)/len(Environment.getPortfolios()["p0"].getCorrectList())
        print "TEST GUESSED    : " , (Environment.getPortfolios()["p0"].getCorrectList().count(1)+Environment.getPortfolios()["p0"].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()["p0"].getCorrectList())
        print "TEST BALANCE    : " ,  Environment.getPortfolios()["p0"].getBalanceList()[-1]

        return (Environment.getPortfolios()["p0"].getCorrectList().count(1)*1.0)/len(Environment.getPortfolios()["p0"].getCorrectList()),Environment.getPortfolios()["p0"].getBalanceList()[-1]

if __name__ == '__main__':
    IndividualTester(TopSpecies)