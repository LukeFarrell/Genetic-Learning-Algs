from sknn.mlp import Regressor, Layer
import csv
import numpy as np
from numpy import average


dayDict = {}
with open('/Users/lukefarrell/Desktop/Stocks/XOM.csv', 'rb') as DataCsv:
    DataDict = csv.DictReader(DataCsv)
    index = 0
    factorNames = DataDict.fieldnames
    for  row in DataDict:
    	dayDict[index] = {}
    	for factor in factorNames:
    		dayDict[index][factor] = row[factor]
    	index += 1
factorNames.remove("Date")

Y = [float(dayDict[day]["close"]) for day in range(1,len(dayDict))]
X = [[float(dayDict[day][factor]) for factor in factorNames] for day in range(len(dayDict)-1)]

days = [day for day in range(len(Y))]
np.random.shuffle(days)
testdays  = days[0:int(.3*len(days))]
traindays = days[int(.3*len(days)):]

y_Train = []
x_Train = []
for day in traindays:
	y_Train.append(Y[day])
	x_Train.append(X[day])

y_Test = []
x_Test = []
for day in testdays:
	y_Test.append(Y[day])
	x_Test.append(X[day])


#Intialize Network Parameters
NumIterations = 10
NumNeurons = 10
Layers = [Layer(type = "Sigmoid", units = 5), Layer(type ="Linear")]
NN = Regressor(
    layers= Layers,
    learning_rate=.05,
    n_iter=NumIterations)

NN.fit(np.array(x_Train), np.array(y_Train))

Error = []
for x in range(len(x_Test)):
	print NN.predict(np.array([x_Test[x]])), y_Test[x]
	Error.append(abs(y_Test - NN.predict(np.array([x_Test[x]]))[0][0]))
print average(Error)
