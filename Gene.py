'''
Created on Jun 24, 2016

@author: Jake
'''
import random
from numpy import average
import numpy as np
import pickle


class Gene(object):
    left=None
    right=None
    delimeter=None
    output=None
    weight=None
    bool=None
    inputs=None
    MUTATION_RATE=0
 
    


    def __init__(self,left,right,delimeter,weight):
        self.MUTATION_RATE=2
        if self.left==None:
            self.left=right
        if self.right==None:
            self.right=left
        if self.delimeter==None:
            self.delimeter=delimeter
        if self.weight==None:
            self.weight=weight
            
        if(self.bool==None):
            if(random.randrange(1,100)) <= self.MUTATION_RATE:
                a=self.mutate(self.right)
                if type(a) !=str:
                    self.right += self.mutate(self.right)
            if(random.randrange(1,100)) <= self.MUTATION_RATE:
                b=self.mutate(self.right)
                if type(b) !=str:
                    self.weight += self.mutate(self.weight)
            if(random.randrange(1,100)) <= self.MUTATION_RATE:
                if(self.delimeter=="<"):
                    self.delimeter=">"
                else:
                    self.delimeter="<"
        
            
    def makeBoolean(self,inputs):
        self.inputs=inputs

        if self.delimeter=="<":
            if type(self.right) is str:
                self.bool = (self.inputs[self.left] < self.inputs[self.right])
            else:
                self.bool = (self.inputs[self.left] < self.right)

        else:
            if type(self.right) is str:
                self.bool = (self.inputs[self.left] > self.inputs[self.right])
            else:
                self.bool = (self.inputs[self.left] > self.right)    
                
    def mutate(self, mutant):
        if type(mutant)==int or type(mutant)==float or type(mutant)==long:
            rand=random.randrange(-5,6)
            rand=rand/100.0
            mutant+=rand
            mutant=round(mutant,3)
        return mutant
    
    def breed(self, gene):
        a=self.getGene()
        b=gene.getGene()
        c=[]
        c.append(Gene(a[2],a[0],a[1],b[3]))
        # c.append(Gene(a[2],a[0],b[1],a[3]))
        c.append(Gene(a[2],a[0],b[1],b[3]))
        c.append(Gene(a[2],b[0],a[1],a[3]))
        # c.append(Gene(a[2],b[0],a[1],b[3]))
        c.append(Gene(a[2],b[0],b[1],a[3]))
        
        d = random.randrange(0,4)
        return c[d]

    def testChildren(self,c):
        a=self.getWombInputs()
        b=self.getWombChange()
        pCorrect=[]
        for gene in c:
            pCorrect.append(0)
        for key in a:
            for gene in range(len(c)):
                c[gene].makeBoolean(a[key])
                f=c[gene].getOutput()
                if((f>0 and b[key]>0) or (f<0 and b[key] <0)):
                    pCorrect[gene]+=1
        m=0
        for x in pCorrect:
            if x>m:
                m=x
        for x in range(len(pCorrect)):
            if x==m:
                return c[x]
        d = random.randrange(0,6)
        return c[d]


    def getWombInputs(self):
        inputListW = pickle.load( open( "inputListW1.p", "rb" ) )
        return inputListW
    def getWombChange(self):
        startPriceListW = pickle.load( open( "startPriceListW1.p", "rb" ) )
        endPriceListW = pickle.load( open( "endPriceListW1.p", "rb" ) )
        changeDict = {}
        for day in endPriceListW:
            changeDict[day] = endPriceListW[day]- startPriceListW[day]
        return changeDict

    def getBool(self):
        return self.bool
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    def getDelimeter(self):
        return self.delimeter
    def getWeight(self):
        return self.weight
    def getGene(self):
        gene=[]
        gene.append(self.left)
        gene.append(self.delimeter)
        gene.append(self.right)
        gene.append(self.weight)
        return gene
    def getOutput(self):
        if(self.bool==True):
            return 1*self.weight
        else:
            return -1*self.weight
    def equals(self,other):
        if(self.left!=other.left):
            return False
        if(self.right!=other.right):
            return False
        if(self.delimeter!=other.delimeter):
            return False
        if(self.weight!=other.weight):
            return False
        return True
if __name__ == '__main__':

    inputs={}
    inputs["a1"]=1
    a1=Gene(.3,"a1","<",.4)
    b1=Gene(.5,"a1",">",.9)
    a1.makeBoolean(inputs)
    b1.makeBoolean(inputs)
    print a1.breed(b1).getGene(),"gene"
    print a1.getBool()
    print a1.getGene()
    print a1.getOutput()
    a=[]
    for x in range(1000):
        a.append(a1.mutate(100))
    print average(a)
    print max(a)
    print min(a)
            
            
        