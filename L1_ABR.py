from sklearn.ensemble import AdaBoostRegressor
import csv
import numpy as np
from numpy import average
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def ModelValuestoValues():
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
    model = AdaBoostRegressor(n_estimators = 100)
    model.fit(x_Train, y_Train)

    Error    = []
    PCorrect = []
    for x in range(len(x_Test)):
        prediction = model.predict(np.array([x_Test[x]]))
    	Error.append(abs(y_Test[x] - model.predict(x_Test[x])))
        if (prediction-Y[testdays[x]-1] > 0 and y_Test[x]-Y[testdays[x]-1] > 0) or (prediction-Y[testdays[x]-1] < 0 and y_Test[x]-Y[testdays[x]-1]< 0):
            PCorrect.append(1)
        else:
            PCorrect.append(0)
    print average(Error), "Error"
    print average(PCorrect), "Percent Correct"

def ModelValuestoDeltas():
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

    Y = [(float(dayDict[day]["Last Price"])-float(dayDict[day-1]["Last Price"])) for day in range(1,len(dayDict))]
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
    model = AdaBoostRegressor(n_estimators = 100)
    model.fit(x_Train, y_Train)

    ErrorL    = []
    PCorrect  = []
    for x in range(len(x_Test)):
        prediction = model.predict(np.array([x_Test[x]]))
        ErrorL.append(abs(y_Test[x] - model.predict(x_Test[x])))
        if (prediction > 0 and y_Test[x] > 0) or (prediction < 0 and y_Test[x] < 0):
            PCorrect.append(1)
        else:
            PCorrect.append(0)
    print average(ErrorL), "Error"
    print average(PCorrect), "Percent Correct"

def ModelDeltastoDeltas():
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

    Y = [(float(dayDict[day]["Last Price"])-float(dayDict[day-1]["Last Price"])) for day in range(2,len(dayDict))]
    X = [[(float(dayDict[day][factor])-float(dayDict[day-1][factor])) for factor in factorNames] for day in range(1,len(dayDict)-1)]

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
    model = AdaBoostRegressor(n_estimators = 100)
    model.fit(x_Train, y_Train)

    ErrorL    = []
    PCorrect  = []
    for x in range(len(x_Test)):
        prediction = model.predict(np.array([x_Test[x]]))
        ErrorL.append(abs(y_Test[x] - model.predict(x_Test[x])))
        if (prediction > 0 and y_Test[x] > 0) or (prediction < 0 and y_Test[x] < 0):
            PCorrect.append(1)
        else:
            PCorrect.append(0)
    print average(ErrorL), "Error"
    print average(PCorrect), "Percent Correct"

if __name__ == "__main__":
    ModelValuestoValues()
    ModelDeltastoDeltas()
    ModelValuestoValues()

