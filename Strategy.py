'''
Created on Jun 21, 2016

@author: Jake
'''
import FirstNodeRunner as FNR
import Portfolio as P
from numpy import std
import matplotlib.pyplot as plt
import numpy as np
import random
from Species import Species
import Gene


class Strategy(object):
    inputs={}
    inputsF={}
    stockList=[]
    #Action is of form (buy/sell/short/buyback, ticker, amount, price)
    recentPrice=0
    endPrice=0
    portfolio={}
    #inputs.get(FirstNodeX)[most recent value, prediction, delta, standard deviation, average error, average percent correct]


    def __init__(self, stockList):
        self.recentPrice=0
        self.endPrice=0
        self.portfolio={}
        self.stockList=stockList
        self.inputs={}
        self.inputsf={}
        
    def setInputs(self,ticker,daysF,daysB):
        a=FNR.setInputsF(ticker,10,daysF,daysB)
        self.inputs=a[0]
        self.endPrice= self.inputs["FirstNodeV"][6][0]
        for x in self.inputs.keys():
            self.recentPrice=self.inputs[x][0]
            break
        self.inputsF=a[1]
        
             
    def addPortfolio(self,name,amount):
        self.portfolio[name]=P.Portfolio(amount)
        
    def getInputs(self):
        return self.inputs
    
    def getRecentPrice(self):
        return self.recentPrice
    
    def getEndPrice(self):
        return self.endPrice
    
    def getPredictions(self):
        predictions=[]
        for key in self.inputs.keys():
            predictions.append(self.inputs[key][1])
        return predictions
    
    def getDeltas(self):
        deltas=[]
        for key in self.inputs.keys():
            deltas.append(self.inputs[key][2])
        return deltas
    def getStd(self):
        std=[]
        for key in self.inputs.keys():
            std.append(self.inputs[key][3])
        return std
    def makeActions(self,p):
        p.makeActions(self.recentPrice)
    def sellBack(self,p):
        p.sellBack(self.stockList,self.endPrice)
    def getError(self):
        error=[]
        for key in self.inputs.keys():
            error.append(self.inputs[key][4])
        return error
    def getPCorrect(self):
        PCorrect=[]
        for key in self.inputs.keys():
            PCorrect.append(self.inputs[key][5])
        return PCorrect
    def getBehaviorList(self):
        return self.behaviorList
    def printPortfolio(self,p):
        p.printAll()
    def getPortfolio(self,p):
        return self.portfolio[p]
    def getPortfolios(self):
        return self.portfolio
    def getInputsF(self):
        return self.inputsF
    
if __name__ == '__main__':
        #Action is of form (Buy/Sell/Short/BuyBack, ticker, amount, price)
    stockList=["LUV"]
    Environment = Strategy(stockList)
    numSpecies=1000
    pInvest=10000
    shareCount=.9
    genCount=4
    DAYS=10
    inputList={}
 
 
#     for d in range(1,DAYS):
#         print "preparing for day",d
#         Environment.setInputs("LUVBBF3", d,d+1 )
#         print Environment.getInputsF()
#         inputList[str(d)]=Environment.getInputsF()
#         print inputList[str(d)]
    p1=P.Portfolio(10000)
    p2=P.Portfolio(10000)
    
    print inputList

    
    

            
        
    for gen in range(genCount):
        for day in range(1,DAYS):
            print "day " + str(day)  +" year "+ str(gen+1)
             
            Environment.setInputs("LUVBBF3", day,day+1 )
    
            inputs=Environment.getInputsF()
            p1.addSpecies(inputs)
            p2.addSpecies(inputs)
            
            p1.getSpecies().addGene(inputs, 'FND4', 'FN1', '>', .93)
            p1.getSpecies().addGene(inputs, 'FND5', -0.4, '>', .21)
            p1.getSpecies().addGene(inputs, 'FN5', 'FNV3', '>', .82)
            p1.getSpecies().addGene(inputs, 'FN4', 'FND3', '>', .58)
            p1.getSpecies().addGene(inputs, 'FN3', 'FND2', '<', .33)
            p1.getSpecies().addGene(inputs, 'FN2', 1.0, '>', .09)
            p1.getSpecies().addGene(inputs, 'FN1', 0.5, '>', .83)
            p1.getSpecies().addGene(inputs, 'FND3', -0.4, '>', .19)
            p1.getSpecies().addGene(inputs, 'FND2', 0.8, '<', .76)
            p1.getSpecies().addGene(inputs, 'FNV2', -0.9, '>', .64)
            p1.getSpecies().addGene(inputs, 'FNV3', -0.8, '>', .59)
            p1.getSpecies().addGene(inputs, 'FNV1', 'FND1', '>', .10)
            p1.getSpecies().addGene(inputs, 'FNV4', 'FNV3', '>', .08)
            p1.getSpecies().addGene(inputs, 'FNV5', 'FND5', '>', .43)
            p1.getSpecies().addGene(inputs, 'FND1', -1.0, '<', .51)
        
            p2.getSpecies().addGene(inputs, 'FND4', 'FN5', '>', .32)
            p2.getSpecies().addGene(inputs, 'FND5', 'FND2', '<', .48)
            p2.getSpecies().addGene(inputs, 'FN5', 'FNV4', '<', .59)
            p2.getSpecies().addGene(inputs, 'FN4', 'FN1', '>', .47)
            p2.getSpecies().addGene(inputs, 'FN3', 0.7, '>', .4)
            p2.getSpecies().addGene(inputs, 'FN2', 0.3, '>', .3)
            p2.getSpecies().addGene(inputs, 'FN1', 'FND2', '<', .57)
            p2.getSpecies().addGene(inputs, 'FND3', 0.1, '>', .29)
            p2.getSpecies().addGene(inputs, 'FND2', 0.8, '>', .52)
            p2.getSpecies().addGene(inputs, 'FNV2', -0.4, '>', .82)
            p2.getSpecies().addGene(inputs, 'FNV3', 'FNV3', '<', .09)
            p2.getSpecies().addGene(inputs, 'FNV1', 'FN1', '>', .67)
            p2.getSpecies().addGene(inputs, 'FNV4', 'FN1', '<', .07)
            p2.getSpecies().addGene(inputs, 'FNV5', -0.6, '<', .09)
            p2.getSpecies().addGene(inputs, 'FND1', 0.9, '<', .34)
#             inputs=inputList[str(day)]
            print inputs
#             print inputList[str(day)]
            print Environment.endPrice
            variables=inputs.keys()
            delimeters=["<",">"]
            right=[[],[]]
            weight=[]
            fitness={}
             
            for x in p1.getSpecies().getGenes():
                print p1.getSpecies().getGenes()[x].getGene()
                print p1.getSpecies().getGenes()[x].getOutput()
            print p1.getSpecies().getOutput(),"output"
             
            for x in p2.getSpecies().getGenes():
                print p2.getSpecies().getGenes()[x].getGene()
                print p2.getSpecies().getGenes()[x].getOutput()
            print p2.getSpecies().getOutput(),"output" 
             
             
             
            p1.addBehavior(p1.getSpecies().getOutput()>.5, ("Buy", "LUV",shareCount*(p1.balance/Environment.recentPrice),Environment.recentPrice))
            p1.addBehavior(p1.getSpecies().getOutput() <-.5, ("Short", "LUV",shareCount*(p1.balance/Environment.recentPrice),Environment.recentPrice))
#             p1.addBehavior(p1.getSpecies().getOutput()<.5 and p1.getSpecies().getOutput() > -.5, ("Buy", "LUV",0,Environment.recentPrice))
            
            p2.addBehavior(p2.getSpecies().getOutput()>.5, ("Buy", "LUV",shareCount*(p2.balance/Environment.recentPrice),Environment.recentPrice))
            p2.addBehavior(p2.getSpecies().getOutput() <-.5, ("Short", "LUV",shareCount*(p2.balance/Environment.recentPrice),Environment.recentPrice))
             
            p1.makeActions(Environment.recentPrice)
            p1.sellBack(stockList,Environment.endPrice)
            
            p2.makeActions(Environment.recentPrice)
            p2.sellBack(stockList,Environment.endPrice)
            print p1.balance,"balance"
            print p2.balance,"balance"
            p1.addBalance(p1.balance)
            p2.addBalance(p2.balance)
            
        plt.plot(p1.balanceList, "g-")
        plt.plot(p2.balanceList, "b-")
        print p1.getSpecies().printSpecies(),"p1"
        print p2.getSpecies().printSpecies(),"p2"

        a = p1.getSpecies().copy()
        b = p2.getSpecies().copy()
        p2.resetAll(10000)

        p2.updateSpecies(a.breed(b))
        p1.reset(10000)
        
        print p1.getSpecies().printSpecies(),"p1"

        print p2.getSpecies().printSpecies(),"p2"
        
        print len(p1.getSpecies().getGenes())
        print len(p2.getSpecies().getGenes())

             

     
    plt.show()