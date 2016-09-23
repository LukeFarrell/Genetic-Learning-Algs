from sklearn import svm
from sklearn.preprocessing import StandardScaler
import csv
import numpy as np
from numpy import average
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


dayDict = {}
with open('/Users/lukefarrell/Desktop/Stocks/LUVBBF4.csv', 'rb') as DataCsv:
    DataDict = csv.DictReader(DataCsv)
    index = 0
    factorNames = DataDict.fieldnames
    for  row in DataDict:
    	dayDict[index] = {}
    	for factor in factorNames:
    		dayDict[index][factor] = row[factor]
    	index += 1
factorNames.remove("Date")

Y = [float(dayDict[day]["Last Price"]) for day in range(1,len(dayDict))]
X = [[float(dayDict[day][factor]) for factor in factorNames] for day in range(len(dayDict)-1)]

days = [day for day in range(801,len(Y))]
np.random.shuffle(days)
testdays  = days[0:int(.3*len(days))]
traindays = days[int(.3*len(days)):]

y_Train = []
x_Train = []
for day in traindays:
	y_Train.append(Y[day])
	x_Train.append([(X[day][factor]-X[day-800][factor]) for factor in range(len(X[day]))])
print x_Train

y_Test = []
x_Test = []
for day in testdays:
	y_Test.append(Y[day])
	x_Test.append([(X[day][factor]-X[day-800][factor]) for factor in range(len(X[day]))])

clf = svm.SVR(kernel="rbf")

scaler = StandardScaler()
scaler.fit_transform(x_Test)
scaler.fit_transform(x_Train)  

clf.fit(x_Train, y_Train)

Error = []
for x in range(len(x_Test)):
    prediction = clf.predict(x_Test[x])
    print prediction, y_Test[x]
    Error.append(abs(y_Test - prediction[0]))
print average(Error)
