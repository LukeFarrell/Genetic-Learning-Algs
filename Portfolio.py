'''
Created on Jun 21, 2016

@author: Jake
'''
from Species import Species
from Gene import Gene

class Portfolio(object):
    stocksLong={}
    stocksShort={}
    transactions={}
    behaviorList={}
    balanceList=[]
    correctList=[]
    shareCountList=[]
    outputList=[]
    geneCorrectList={}
    inputList={}
    startPriceList={}
    endPriceList={}
    balance=0
    species=None

    def __init__(self,balance):
        self.balance=balance
        self.balanceList=[]
        self.addBalance(balance)
        self.stocksLong={}
        self.stocksShort={}
        self.transactions={}
        self.behaviorList={}
        self.correctList=[]
        self.species=None
        self.inputList={}
    
    def buyStock(self,ticker,amount,price):
        if self.balance-(amount*price)<0:
            # print self.balance, amount, price, self.getShareFactor(),self.balance-(amount*price)
            return 0
        self.balance-=amount*price
        if ticker not in self.stocksLong.keys():
            self.stocksLong[ticker]=0
        self.stocksLong[ticker]+=amount
        if ticker not in self.transactions.keys():
            self.transactions[ticker]=[]
        self.transactions[ticker].append(("BUY",ticker,amount,price))

    def sellStock(self,ticker,amount,price):
        if ticker not in self.stocksLong.keys():
            print "Stock not owned.",ticker
            return 0
        if self.stocksLong[ticker]-amount <0:
            print "Tried to sell more than owned."
            return 0
        self.stocksLong[ticker]-=amount
        self.transactions[ticker].append(("SELL",ticker,amount,price))
        self.balance+=amount*price
        if self.stocksLong[ticker]==0:
            self.stocksLong.pop(ticker)
            
    def shortStock(self,ticker,amount,price):
        if self.balance-(amount*price)<0:
            return 0
        self.balance+=amount*price
        if ticker not in self.stocksShort.keys():
            self.stocksShort[ticker]=0
        self.stocksShort[ticker]+=amount
        if ticker not in self.transactions.keys():
            self.transactions[ticker]=[]
        self.transactions[ticker].append(("SHORT",ticker,amount,price))
        
    def buyBack(self,ticker,amount,price):
        if ticker not in self.stocksShort.keys():
            print "Stock not owned."
            return 0
        if self.stocksShort[ticker]-amount <0:
            print "Tried to sell more than owned."
            return 0
        self.stocksShort[ticker]-=amount
        self.transactions[ticker].append(("BUY BACK",ticker,amount,price))
        self.balance-=amount*price
        if self.stocksShort[ticker]==0:
            self.stocksShort.pop(ticker)
            
        
    def addBehavior(self,boolean,action):
        self.behaviorList[boolean]=action
        
    def makeActions(self,recentPrice):
        for key in self.behaviorList.keys():
            if(key):
                if(self.behaviorList[key][0]=="Buy"):
                    self.buyStock(self.behaviorList[key][1], self.behaviorList[key][2],recentPrice)
                if(self.behaviorList[key][0]=="Sell"):
                    self.sellStock(self.behaviorList[key][1], self.behaviorList[key][2],recentPrice)
                if(self.behaviorList[key][0]=="Short"):
                    self.shortStock(self.behaviorList[key][1], self.behaviorList[key][2],recentPrice)
                if(self.behaviorList[key][0]=="BuyBack"):
                    self.buyBackStock(self.behaviorList[key][1], self.behaviorList[key][2],recentPrice)  
    def sellBack(self,stockList,endPrice):
        for stock in stockList:
            while len(self.getLongHoldings().keys())>0:
                a=self.getLongHoldings().keys()
                self.sellStock(stock, self.getLongHoldings()[a[0]], endPrice)
            while len(self.getShortHoldings().keys())>0:
                a=self.getShortHoldings().keys()
                self.buyBack(stock, self.getShortHoldings()[a[0]], endPrice)   

    def addBalance(self,amount):
        if(len(self.balanceList)>0):
            if(amount>self.balanceList[-1]):
                self.correctList.append(1)
            elif(amount<self.balanceList[-1]):
                self.correctList.append(-1)
            else:
                self.correctList.append(0)
        self.balanceList.append(amount)
    def getBalanceList(self):
        return self.balanceList
    def getReturns(self):
        return self.balanceList[-1]-self.balanceList[0]
    def getMaxReturns(self):
        return max(self.balanceList)-self.balanceList[0]
    def getCorrectList(self):
        return self.correctList
    def addSpecies(self,inputs):
        self.species=Species(inputs)
    def getSpecies(self):
        return self.species
    def updateSpecies(self,species):
        self.species=None
        self.species=species           
    def addGeneCorrect(self, change):
        for gene in self.species.genes:
            if gene not in self.geneCorrectList or type(self.geneCorrectList[gene])!=[]:
                self.geneCorrectList[gene]=[]
        for gene in self.species.genes:
            if(change>0):
                if(self.species.genes[gene].getOutput() > 0):
                    self.geneCorrectList[gene].append(1)
                else:
                    self.geneCorrectList[gene].append(0)
            else:
                if(self.species.genes[gene].getOutput()<0):
                    self.geneCorrectList[gene].append(1)
                else:
                    self.geneCorrectList[gene].append(0)

    def getGeneCorrect(self):
        return self.geneCorrectList      
    #get everything     
    def getLongHoldings(self):
        return self.stocksLong
    def getShortHoldings(self):
        return self.stocksShort
    def getTransactions(self):
        return self.transactions
    def getBalance(self):
        return self.balance
    
    #print everything
    def printHoldings(self):
        return "Long Holdings: " + str(self.stocksLong) + "\nShort Holdings: " + str(self.stocksShort)
    def printTransactions(self):
        return "Transactions: " + str(self.transactions)
    def printBalance(self):
        return "Balance: $" + str(self.balance)
    def resetAll(self,balance):
        self.balance=balance
        self.balanceList=[]
        self.correctList = []
        self.addBalance(balance)
        self.stocksLong={}
        self.stocksShort={}
        self.transactions={}
        self.behaviorList={}
        self.species=None
        self.correctList=[]
        self.geneCorrectList = {}
        self.shareCountList=[]
        self.outputList=[]
        
    def reset(self,balance):
        self.balanceList=[]
        self.correctList=[]
        self.balance=balance
        self.behaviorList={}
        self.addBalance(balance)
        self.stocksLong={}
        self.stocksShort={}
        self.transactions={}
        
    def printAll(self):
        print self.printHoldings()
        print self.printTransactions()
        print self.printBalance()
        print self.getSpecies().printSpecies()
    def getShareFactor(self):
        a = self.getSpecies().getShareFactor()
        b = self.getSpecies().getOutput()
        if(b==0):
            return 0.1
        if (a==0):
            return 0.1
        self.shareCountList.append((1.0/a)**(1.0/abs(b)))
        self.outputList.append(self.species.getOutput())
        return (1.0/a)**(1.0/abs(b))
    def getShareCountList(self):
        return self.shareCountList
    def getOutputList(self):
        return self.outputList
    def copy(self):
    #      stocksLong={}
    # stocksShort={}
    # transactions={}
    # behaviorList={}
    # balanceList=[]
    # correctList=[]
    # shareCountList=[]
    # outputList=[]
    # geneCorrectList={}
    # inputList={}
    # startPriceList={}
    # endPriceList={}
    # balance=0
    # species=None

        a = Portfolio(self.balance)
        a.balanceList=self.balanceList.copy()
        a.correctList=self.correctList.copy()
        a.behaviorList=self.behaviorList.copy()
        a.shareCountList=self.shareCountList.copy()
        a.species=self.species.copy()
        a.outputList=self.outputList.copy()
        a.geneCorrectList=self.geneCorrectList.copy()
        a.inputList=self.inputList.copy()
        a.startPriceList=self.startPriceList.copy()
        a.endPriceList=self.endPriceList.copy()
        a.transactions=self.transactions.copy()

        return a


        
if __name__ == '__main__':
    p1=Portfolio(10000)
    p1.buyStock("AAPL",10,80)
    p1.shortStock("LUV", 10, 43)
    p1.printAll()
    
    p1.sellStock("AAPL",10,100)
    p1.buyBack("LUV", 10, 30)
    p1.sellBack(["AAPL"], 100)
    p1.printAll()
    


            

        