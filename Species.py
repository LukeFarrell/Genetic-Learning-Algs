'''
Created on Jun 24, 2016

@author: Jake
'''
from Gene import Gene
import random

class Species(object):
    inputs={}
    genes={}
    out=0
    leftThresh=0
    rightThresh=0
    shareFactor=0
    inputList={}
    startPriceList={}
    endPriceList={}
    MUTATION_RATE=5
    #gene is of form Gene(inputs,left,right,delimeter,weight)

    def __init__(self, inputs):
        self.MUTATION_RATE=5
        self.inputs=inputs
        self.out=0
        self.inputList={}
        self.genes={}
        for x in inputs.keys():
            self.genes[x]=None
    def addGene(self,left,right,delimeter,weight):
        self.genes[left]=(Gene(right,left,delimeter,weight))
    
    def breed(self,species):
        c=Species(self.inputs)
        for x in self.genes.keys():
            c.genes[x]=self.genes[x].breed(species.genes[x])
        d=[]
        d.append((self.getLeftThresh(),c.getRightThresh()))
        d.append((c.getLeftThresh(),self.getRightThresh()))
        e=d[random.randrange(0,2)]
        c.setThresh(e[0],e[1])
        d=[]
        d.append(self.getShareFactor())
        d.append(species.getShareFactor())
        e=d[random.randrange(0,2)]
        c.setShareFactor(e)
        return c
    def getOutput(self):
        out=0
        for x in self.genes.keys():
            a=self.genes[x].getOutput()
            out+= a
        return out
    def getGenes(self):
        return self.genes
    def getOut(self):
        return self.out
    def printSpecies(self):
        s=[]
        for gene in self.genes:
            s.append(self.genes[gene].getGene())
        s.append(self.leftThresh)
        s.append(self.rightThresh)
        s.append(self.shareFactor)
        return s
    def copy(self):
        inputsc={}
        genesc={}
        for x in self.inputs.keys():
            inputsc[x]=self.inputs[x]
        c=Species(inputsc)
        for x in self.genes.keys():
            genesc[x]=self.genes[x]
        for x in genesc.keys():
            y=genesc[x]
            c.addGene(y.left,y.right,y.delimeter,y.weight)
        c.setThresh(self.getLeftThresh(),self.getRightThresh())
        c.setShareFactor(self.getShareFactor())
        return c
    def setThresh(self,left,right):
        self.leftThresh=self.mutate(left)
        self.rightThresh=self.mutate(right)

    def setShareFactor(self,fact):
        self.shareFactor=fact

        a=random.randrange(1,100)
        b=random.randrange(0,2)

        if(a<=self.MUTATION_RATE):
            if(a%2==0):
                self.shareFactor+=.05

            else:
                if(self.shareFactor>1.05):
                    self.shareFactor-=.05
    def mutate(self,mutant):
        a=random.randrange(0,100)
        b=random.randrange(0,2)

        if(a<=self.MUTATION_RATE):
            if(a%2==0):
                if(b==0):
                    mutant+=.05
                else:
                    mutant-=.05
            else:
                if(b==0):
                    mutant+=.05
                else:
                    mutant-=.05
        return mutant


    def getRightThresh(self):
        return self.rightThresh
    def getLeftThresh(self):
        return self.leftThresh
    def getShareFactor(self):
        return self.shareFactor
    def equals(self,other):
        # if self.leftThresh!=other.leftThresh:
        #     return False
        # if self.rightThresh!=other.rightThresh:
        #     return False
        # if self.shareFactor!=other.shareFactor:
        #     return False

        for x in self.getGenes().keys():
            if(not (self.getGenes()[x].equals(other.getGenes()[x]))):
                return False
        return True
    def numEquals(self,other):
        count=0
        for x in self.getGenes().keys():
            if((self.getGenes()[x].equals(other.getGenes()[x]))):
                count+=1
        return count 




    

         
         
 
     
        