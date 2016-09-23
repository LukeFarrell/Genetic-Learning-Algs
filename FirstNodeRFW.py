import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from numpy import average
import warnings

def train(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,end):
    
#   Gets data from file and converts to 2D array
    csv = np.genfromtxt (ticker+'.csv', delimiter=",")
    
#   Gets only columns and rows we want from array
    newCsv=csv[:,startCol:endCol][startRow:]
    
#   Finds number of columns being used
    numFactors=len(newCsv[0])
    
#   Creates array of 0's size we need
    X = [[0 for x in range(numFactors)] for y in range(numDataPoints)] 
    
#   Places values in array of deltas of -1st date to -1 - window days back numDataPoints number of times
    for factor in range(0,numFactors):
        for day in range (0,numDataPoints):
            X[day][factor]= newCsv[-1-daysForward-day][factor]-newCsv[-1-daysForward-day-window][factor]

#   Makes target Vector
    y=csv[:,targetCol][len(csv)-numDataPoints:]

    y=np.ndarray.tolist(y)
    dicty=[]
    for x in y:
        dicty.append(x)
#   Remove and set aside data points for testing
    testX=[]
    testY=[]
    yBack = []
    xBack = []
    for x in range(daysBackward):
        xBack.append(X.pop(len(X)-1))
        yBack.append(y.pop(len(y)-1))
    
    for x in range(len(randL)):
        testX.append(X[randL[x]])
        testY.append(y[randL[x]])
        X[randL[x]]=10e36
        y[randL[x]]=10e36
    
    for x in range(len(randL)):
        X.remove(10e36)
        y.remove(10e36)
    
    y=y[::-1]
    Start=0
    Y = []
    for day in range(len(y)):
        if day == 0:
            Start= y[day]

    yBack = yBack[::-1]
        
    Z = [[0 for l in range(numFactors)] for j in range(numDataPoints)] 
    for col in range(0,numFactors):
        for day in range (0,numDataPoints):
            Z[day][col]= newCsv[-1-day][col]-newCsv[-1-day-window][col]

    if end:
        Z = [[0 for l in range(numFactors)] for j in range(numDataPoints)] 
        for col in range(0,numFactors):
            for day in range (0,numDataPoints):
                Z[day][col]= newCsv[-daysForward-day][col]-newCsv[-daysForward-day-window][col]
        testX[-1] = Z[0]
            
        
    #Train model
    clf = RandomForestRegressor(n_estimators = 10)
    X=np.asarray(X)
    y=np.asarray(y)

#   Test Model
    scaler = StandardScaler()
    scaler.fit_transform(testX)
    scaler.fit(X)  

    X_train = scaler.transform(X)
    clf.fit(X_train, y)

  
    exper = []
    act = []
    testY = np.array(testY).reshape((len(testY), 1))
    warnings.filterwarnings("ignore", category=DeprecationWarning) 


    for x in testX:  
        exper.append(clf.predict(x))
    for y in testY:
        act.append(y)

    #Make Mega Dictionary 
    D = {}
    for x in range(len(randL)):
        D[randL[x]] = exper[x][0],act[x][0]
    
    Xback = scaler.transform(xBack)
    predictions = []
    predictions.append(clf.predict(Xback[0])[0])
        
#     Error = []
#     for x in range(len(predictions)):
#         Error.append((yBack[x]-predictions[x])/abs(yBack[x]))

    errorGL = []
    percent = []
    for x in range(len(exper)):
        today = randL[x]
        todayG = exper[x]
        todayA = dicty[today]
        yesterday = dicty[today-daysForward]
         
        errorG = abs(todayG - todayA)
        errorGL.append(errorG/todayA)
         
        dA= todayA - yesterday
        dG= todayG - yesterday
         
        if (dA < 0 and dG < 0) or (dA >0 and dG>0):
            percent.append(1)
        else:
            percent.append(0)
    
#     print average(percent)
    
#   Return Prediction     
#     print average(percent), average(errorGL)
#     return average(percent), average(errorGL)
    for x in range(len(exper)):
        exper[x]=exper[x][0]
    for x in range(len(act)):
        act[x]=act[x][0]
        
    return exper,act, errorGL, predictions[0], yBack, average(percent), Start

                                                       
if __name__ == '__main__':

    window = 100
    daysBackward=45
    daysForward = 45
    predict = []
    error = []
    yBack =[]
    for z in range(1,daysForward):
        randL = []
        for y in range(1,int(300-window-daysBackward)):
            randL.append(y)
            np.random.shuffle(randL)
#
#        perc=[]
#   train("MMMBB",500,1,2,16,1,1700,1,randL[0:int(len(randL)*.3)],True)
        a = train("LUVBBF3",window,1,2,16,1,300-window,z,daysBackward,randL[0:int(len(randL)*.3)],True)
##
        predict.append(a[3])
        print predict
        error.append(a[2])

    yBack.append(a[4])
    print yBack
    plt.plot(predict,"b--")
    plt.plot(yBack[0],"g-")

    plt.show()
    
    print average(error)
    
    print "done"
    