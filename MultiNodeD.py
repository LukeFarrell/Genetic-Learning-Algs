'''
Created on May 22, 2016

@author: Jake Shulman & Luke Farrell
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from numpy import average
import FirstNodeD as FirstNode
import time
import Tkinter as tkinter
import tkFileDialog
import csv
import smtplib
import email
    
def trainMulti(ticker,window,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,numNodes):   

    trainX=[]
    trainY=[]
    testX=[]
    yBack = []
#     error = []
    randL = []
    
    start_time = time.time()
    
    for x in range(1,int(numDataPoints-daysBackward-daysForward)):
        randL.append(x)
    np.random.shuffle(randL)
    print "Step 1"
    
    for x in range(1,numNodes):
        trainX.append(FirstNode.train(ticker,x,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[0:int((len(randL)*.35))],False)[0])
    print "Step 2"
    
    v=[] 
    for x in range(1,numNodes):
        v.append(FirstNode.train(ticker,x,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[int((len(randL)*.35)):int((len(randL)*.7))],False)[0])
        print "running.."
        
    print "Step 3"
    
    for x in range(1,numNodes):
        testX.append(FirstNode.train(ticker,x,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL[int((len(randL)*.7)):],True)[0])
        print "running...."
        
    trainY.append(FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)[1])
    print "Step 4"
    yBack.append(FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)[3])    

    
    trainXF=[]
    for x in range(len(trainX)):
        trainXF.append(trainX[x]+v[x])

    print "Training..."

    trainRXF=zip(*trainXF[::-1])
    testRX = zip(*testX[::-1])
    
    trainYF=trainY[0][0:len(trainRXF)]
    testY=trainY[0][len(trainRXF):]

    
    clf = svm.SVR(kernel="linear")

    clf.fit(trainRXF, trainYF)
    print "fit!"
    
    predictions=[]
    for x in testRX:
        predictions.append(clf.predict(x))
        


    
#    for x in range(len(predictions)):
#        error.append(abs(predictions[x]-testY[x])/testY[x])
#    print average(error)
##    plt.plot(predictions,"g-")
##    plt.plot(testY,"b-")
##    plt.show()
#    
#    errorGL = []
#    percent = []
    
    print predictions[-1],"-1"  
    randL.remove(len(randL))
#    for x in range(len(predictions)):
#        today = randL[x]
#        todayG = predictions[x]
#        todayA = trainY[0][today]
#        yesterday = trainY[0][today-daysForward]
#         
#        errorG = abs(todayG - todayA)
#        errorGL.append(errorG)
#         
#        dA= todayA - yesterday
#        dG= todayG - yesterday
#         
#        if (dA < 0 and dG < 0) or (dA >0 and dG>0):
#            percent.append(1)
#        else:
#            percent.append(0)
#            
#
#    print percent.count(1)/(len(percent)*1.0)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print "done"
    
  
    
    PREDICTION = predictions[-1][0]
    PERCENT = 0
    ERROR = 0
    
    
    print trainX, "TrainX"
    print trainY, "TrainY"
    
# EMAIL EMAIL EMAIL
#        # Credentials
#    username = 'luke.farrell32197@gmail.com'  
#    password = 'Jenna321'
#
# 
#    From = 'luke.farrell32197@gmail.com'  
#    Recipient  = ['jacobashulman@gmail.com','luke.farrell32197@gmail.com']
##    Message = (ticker+":  "+"PREDICTION"+str(predictions[0][-1]))
#    subject = str(ticker[0:len(ticker)-3])
#    body = ("PREDICTION:  "+str(predictions[0][-1]))
#    
#    email_text = """\  
#    Subject: %s
#    
#    %s
#    """ % (subject, body)
#    
     
    
      
    # mail is being sent :  
#    server = smtplib.SMTP('smtp.gmail.com:587')  
#    
#    
#    server.starttls()  
#    
#    server.login(username,password)  
#    
#    server.sendmail(From, Recipient, email_text)  
#    server.quit() 
#    
#    "EMAIL SENT!"
    
    return PREDICTION, PERCENT, ERROR, yBack
#    beep(sys.argv[1])
#    winsound.Beep(Freq,Dur)
#    time.sleep(1)
#    winsound.Beep(Freq,Dur)


    
        
    
#     print int(len(randL)*.35)
#     print int(len(randL)*.7)
#     print randL
#     print len(trainX)
#     print len(trainX[0])
#     print (trainY[0])
#     print len(trainY[0])
#     plt.plot(trainX[:,0],"g-")
#     plt.plot(trainY,"b-")


#     return , error



if __name__ == '__main__':
    timeS = time.time()
    daysForward = 2

    for z in range(1,2):
        predictions= []
        percent = []
        error = []
        yBack = []
        for F in range(1,daysForward):        
            ticker="LUVBBF"
            window= 10
            startRow=1
            startCol=2
            endCol=23
            targetCol=1
            daysForward= F
            daysBackward = 45
            numNodes=window
            numDataPoints=2000-window
            
            a = trainMulti(ticker, window, startRow, startCol, endCol, targetCol, numDataPoints, daysForward, daysBackward, numNodes)
            predictions.append(a[0])
        predictions = predictions[::-1]
        yBack.append(a[3])  
        
    Start = yBack[0][0]
    print Start
    Error= []
    predictionsF = []
    for x in range(len(predictions)):
        Start =Start+ predictions[x]
        predictionsF.append(Start)
    
    print predictionsF, "PREDICTIONS"
    plt.plot(yBack[0][0:len(predictionsF)], "g-")
    plt.plot(predictionsF,"b--")
    plt.show()
    
    for day in range(len(predictionsF)):
        if day!= 0:
            Error.append(abs((yBack[0][day]-predictionsF[day])/yBack[0][day]))
    print Error, "ERRORS"
    print average(Error), "AVG ERROR"
        
    timeFF = time.time()
    final_time = timeFF - timeS
    print "----------"+str(final_time)+"------------"

    
    print "done"