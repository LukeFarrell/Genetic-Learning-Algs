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



if __name__ == '__main__':
    stockList=["LUV"]
    avg=[]
    mx=[]
    graph={}
    g=[]
    TOPV=0
    TOP=0
    

            
    Environment = Strategy(stockList)
    numSpecies=1000
    pInvest=10000
    shareCount=.8
    genCount=2
    DAYS=5
    inputList={}
    startPriceList={}
    endPriceList={}
    
#Make Portfolios

    for individual in range(numSpecies):
        Environment.addPortfolio("p"+str(individual),pInvest)

#Set inputList

    for d in range(1,DAYS):
        print "preparing for day",d
        Environment.setInputs("LUVBBF3", d,d+1 )
        inputList[d]=(Environment.getInputsF().copy())
        startPriceList[d]=Environment.getRecentPrice()
        endPriceList[d]=Environment.getEndPrice()
    
    
#Make lists for randomization of initial population

    inputs=inputList[1]
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
            
# Start loop of days and generations     
        
    for gen in range(genCount):
        for day in range(1,DAYS):
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
                Environment.getPortfolios()[portfolio].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() >.5, ("Buy", "LUV",shareCount*(Environment.getPortfolios()[portfolio].balance/startPrice),startPrice))
                Environment.getPortfolios()[portfolio].addBehavior(Environment.getPortfolios()[portfolio].getSpecies().getOutput() <-.5, ("Short", "LUV",shareCount*(Environment.getPortfolios()[portfolio].balance/startPrice),startPrice))
                Environment.getPortfolios()[portfolio].addGeneCorrect(endPrice-startPrice)

#Go through with actions, sellBack at end of day and add balance to balanceList

            for portfolio in Environment.getPortfolios().keys():
                Environment.getPortfolios()[portfolio].makeActions(startPrice)
                Environment.getPortfolios()[portfolio].sellBack(stockList,endPrice)
                Environment.getPortfolios()[portfolio].addBalance(Environment.getPortfolios()[portfolio].balance)  

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

                
#Add balanceList to graph
    
        # for portfolio in Environment.getPortfolios().keys():
        #     plt.plot(Environment.getPortfolios()[portfolio].getBalanceList())
            
    print TOPV
    print Environment.getPortfolios()[TOP].getSpecies().printSpecies()
    print (Environment.getPortfolios()[TOP].getCorrectList().count(1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList()),"CORRECT"
    print (Environment.getPortfolios()[TOP].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList()),"INCORRECT"
    print (Environment.getPortfolios()[TOP].getCorrectList().count(0)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList()),"HELD"
    print (Environment.getPortfolios()[TOP].getCorrectList().count(1)+Environment.getPortfolios()[TOP].getCorrectList().count(-1)*1.0)/len(Environment.getPortfolios()[TOP].getCorrectList()),"GUESSED"
    print Environment.getPortfolios()[TOP].getBalanceList()[-2],"BALANCE"

    for gene in Environment.getPortfolios()[TOP].getGeneCorrect():
        Environment.getPortfolios()[TOP].getGeneCorrect()[gene]=((sum(Environment.getPortfolios()[TOP].getGeneCorrect()[gene])*1.0)/len(Environment.getPortfolios()[TOP].getGeneCorrect()[gene]))
    plt.bar(range(len(Environment.getPortfolios()[TOP].getGeneCorrect())), Environment.getPortfolios()[TOP].getGeneCorrect().values(), align='center')
    plt.xticks(range(len(Environment.getPortfolios()[TOP].getGeneCorrect())), Environment.getPortfolios()[TOP].getGeneCorrect().keys())
    plt.show()
    # plt.show()
    # plt.plot(Environment.getPortfolios()[TOP].getBalanceList())      
    # plt.show()  


