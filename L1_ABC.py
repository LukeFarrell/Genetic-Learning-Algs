from sklearn.ensemble import AdaBoostClassifier
import csv
import numpy as np
from numpy import average
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 



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

    Y= []
    for day in range(2,len(dayDict)):
            if (float(dayDict[day]["Last Price"])-float(dayDict[day-1]["Last Price"])> 0):
                Y.append(1)
            else:
                Y.append(-1)

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
    model = AdaBoostClassifier(n_estimators = 100, )
    model.fit(x_Train, y_Train)

    ErrorL    = []
    PCorrect  = []
    for x in range(len(x_Test)):
        prediction = model.predict(np.array([x_Test[x]]))
        print prediction, y_Test[x]
        ErrorL.append(abs(y_Test[x] - model.predict(x_Test[x])))
        if (prediction > 0 and y_Test[x] > 0) or (prediction < 0 and y_Test[x] < 0):
            PCorrect.append(1)
        else:
            PCorrect.append(0)
    print average(ErrorL), "Error"
    return average(PCorrect)



if __name__ == "__main__":
    A = []
    for x in range(10):
        A.append(ModelDeltastoDeltas())
    print average(A)




