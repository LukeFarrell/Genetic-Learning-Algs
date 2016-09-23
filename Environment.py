'''
Created on Jun 25, 2016

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

            
    Environment = Strategy(stockList)
    numSpecies=100
    pInvest=10000
    shareCount=.9
    genCount=10
    DAYS=3
    inputList={}
    
    for individual in range(numSpecies):
        Environment.addPortfolio("p"+str(individual),pInvest)
#     for portfolio in Environment.getPortfolios():
#         Environment.getPortfolios()[portfolio].addSpecies({})
    
    
#     for d in range(1,DAYS):
#         print "preparing for day",d
#         Environment.setInputs("LUVBBF3", d,d+1 )
#         print Environment.getInputsF()
#         inputList[str(d)]=Environment.getInputsF()
#         print inputList[str(d)]
       
for gen in range(genCount):
    for day in range(1,DAYS):
        print "day " + str(day)  +" year "+ str(gen+1)
        
        Environment.setInputs("LUVBBF3", day,day+1 )
        inputs=Environment.getInputsF()
#         inputs=inputList[str(day)]
#         print inputs
#         print inputList[str(day)]
#         print Environment.endPrice
        variables=inputs.keys()
        delimeters=["<",">"]
        right=[[],[]]
        weight=[]
        fitness={}
     
        for x in np.arange(-1,1.1,.1):
            right[0].append(round(x,2))
        for y in variables:
            right[1].append(y)    
        for z in np.arange(0,1,.01):
            weight.append(round(z,3))
         
 
        for portfolio in Environment.getPortfolios().keys():
#             if Environment.getPortfolios()[portfolio].getSpecies().getGenes()=={}:
                p = Environment.getPortfolios()[portfolio]
                p.addSpecies(inputs)
                for variable in Environment.getPortfolios()[portfolio].getSpecies().getGenes().keys():
                    a=random.randint(0,1)
                    b=random.randint(0,len(right[a])-1)
                    c=delimeters[random.randint(0,1)]
                    d=weight[random.randint(0,99)]
                    Environment.getPortfolios()[portfolio].getSpecies().addGene(inputs,variable,right[a][b],c,d)
                 
     
                Environment.getPortfolios()[portfolio].addBehavior(p.getSpecies().getOutput() >.5, ("Buy", "LUV",shareCount*(Environment.getPortfolios()[portfolio].balance/Environment.recentPrice),Environment.recentPrice))
                Environment.getPortfolios()[portfolio].addBehavior(p.getSpecies().getOutput() <-.5, ("Short", "LUV",shareCount*(Environment.getPortfolios()[portfolio].balance/Environment.recentPrice),Environment.recentPrice))
                Environment.getPortfolios()[portfolio].addBehavior(p.getSpecies().getOutput() <.5 and p.getSpecies().getOutput() > -.5, ("Buy", "LUV",0,Environment.recentPrice))
 
 
         
        for portfolio in Environment.getPortfolios().keys():
            Environment.getPortfolios()[portfolio].makeActions(Environment.recentPrice)
            Environment.getPortfolios()[portfolio].sellBack(stockList,Environment.endPrice)
#             print Environment.getPortfolios()[portfolio].balance,"balance"
            Environment.getPortfolios()[portfolio].addBalance(Environment.getPortfolios()[portfolio].balance) 
 
    for portfolio in Environment.getPortfolios().keys():
        fitness[portfolio]=Environment.getPortfolios()[portfolio].balanceList[-2]
        graph[portfolio]=Environment.getPortfolios()[portfolio].getBalanceList()
         
 
    for x in graph:
        plt.plot(graph[x])
        g+=graph[x]
 
         
    #sort by fitness[key]
    sorted_fitness = sorted(fitness.items(), key=operator.itemgetter(1))
    
    if(sorted_fitness[-1][-1]>TOPV):
        TOP=sorted_fitness[-1][0]
        TOPV=sorted_fitness[-1][1]
     
     
    #get list of 50 worst 
    bottom=sorted_fitness[0:(numSpecies/2)]
     
    #choose 50 pairs of top 50
    top=sorted_fitness[numSpecies/2:numSpecies]
    topPair=[]
    for x in range(len(top)):
        pair=x
        while top[pair][0]==top[x][0]:
            pair=random.randint(0,len(top)-1)
        topPair.append((top[x][0],top[pair][0]))
    print topPair
 
     
#     print fitness.values()
#     for x in fitness.keys():
#         if fitness[x]==a:
#             print Environment.getPortfolios()[x].getSpecies().printSpecies(),"WINNER WINNER, CHICKEN DINNER"
    a= max(fitness.values())
    avg.append(average(fitness.values()))
    mx.append(max(fitness.values()))
 
     
#     print "all"
#     for x in Environment.getPortfolios().keys():
#         print Environment.getPortfolios()[x].getSpecies().printSpecies()
#     
#     print "top"  
#     print
#     for x in range(len(top)):
#         print top
#         print Environment.getPortfolios()[top[x][0]].getSpecies().printSpecies()
#     print "bottom"
#     print
     
#     for x in range(len(bottom)):
#         print Environment.getPortfolios()[bottom[x][0]].getSpecies().printSpecies()
     
    #for portfolio in 50 worst, set it equal to the breeding of a pair of top 50
    for x in range(len(bottom)):
        a = Environment.getPortfolios()[topPair[x][0]].getSpecies().copy()
        b=Environment.getPortfolios()[topPair[x][1]].getSpecies().copy()

        Environment.getPortfolios()[bottom[x][0]].resetAll(pInvest)
        Environment.getPortfolios()[bottom[x][0]].updateSpecies(a.breed(b).copy())

    for x in range(len(top)):
        Environment.getPortfolios()[top[x][0]].reset(pInvest)
    
    print (Environment.getPortfolios()["p1"].getSpecies().printSpecies()),"len p1"
    print (Environment.getPortfolios()["p2"].getSpecies().printSpecies()),"len p2"
    print (Environment.getPortfolios()["p3"].getSpecies().printSpecies()),"len p3"

 
     
#     print "end"
#     print
#     for x in Environment.getPortfolios().keys():
#         print Environment.getPortfolios()[x].balanceList
     
 
    #graph/do analysis/print values
     
print "best"
print TOPV
print Environment.getPortfolios()[TOP].getSpecies().printSpecies()
plt.show()
 
plt.plot(avg)
plt.show()
plt.plot(mx)
plt.show()
plt.plot(g)
plt.show()
 
 
 


