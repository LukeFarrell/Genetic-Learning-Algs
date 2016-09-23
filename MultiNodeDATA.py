'''
Created on May 22, 2016

@author: Jake Shulman & Luke Farrell
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from numpy import average
import FirstNode
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
#     error = []
    randL = []
    
    start_time = time.time()
    


    
    for x in range(daysBackward+daysForward+4,numDataPoints):
        print x,"HELLO:"
        randL = []
        for y in range(1,int(x-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        trainX.append(FirstNode.train(ticker,window,startRow,startCol,endCol,targetCol,x,daysForward,daysBackward,randL[0:int((len(randL)*.35))],False)[0])
    print "Step 2"
    
    v=[] 
    for x in range(daysBackward+daysForward+4,numDataPoints):
        randL = []
        for y in range(1,int(x-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        v.append(FirstNode.train(ticker,window,startRow,startCol,endCol,targetCol,x,daysForward,daysBackward,randL[int((len(randL)*.35)):int((len(randL)*.7))],False)[0])
        print "running.."
        
    print "Step 3"
    
    for x in range(daysBackward+daysForward+4,numDataPoints):
        randL = []
        for y in range(1,int(x-daysBackward-1)):
            randL.append(y)
            np.random.shuffle(randL)
        testX.append(FirstNode.train(ticker,window,startRow,startCol,endCol,targetCol,x,daysForward,daysBackward,randL[int((len(randL)*.7)):],True)[0])
        print "running...."
        
    trainY.append(FirstNode.train(ticker,1,startRow,startCol,endCol,targetCol,numDataPoints,daysForward,daysBackward,randL,False)[1])
    print "Step 4"
    
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
    
    print trainX, "TrainX"
    for x in testRX:
        predictions.append(clf.predict(x))

    #.writerow(str(ticker) + ':   Days Forward: ' + str(daysForward)+   'Window Size: ' +str(window))
  #  f.writerow('PREDICTION:  ' + str(predictions[-1]))
    print predictions    
    error = []
    for x in range(len(predictions)):
        error.append(abs(predictions[x]-testY[x])/testY[x])
    print error
#    plt.plot(predictions,"g-")
#    plt.plot(testY,"b-")
#    plt.show()
    
    percent = []
    
    print len(predictions) , "PREDICTIONS"
    randL.remove(len(randL))
    for x in range(len(predictions)):
        today = randL[x]
        todayG = predictions[x]
        todayA = trainY[0][today]
        yesterday = trainY[0][today-daysForward]

        dA= todayA - yesterday
        dG= todayG - yesterday
         
        if (dA < 0 and dG < 0) or (dA >0 and dG>0):
            percent.append(1)
        else:
            percent.append(0)
            

    print percent.count(1)/(len(percent)*1.0)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print "done"
    
    PREDICTION = predictions[-1]
    PERCENT = (percent.count(1)/(len(percent)*1.0))*1.0
    ERROR = average(error)
    
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
    
    return PREDICTION, PERCENT, ERROR
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
    numDaysForward = 1
    numDatatPoints = 500
    predictions= []
    percent = []
    error = []
    for w in range(55,numDatatPoints,100):        
        ticker="JNJBBF"
        window= 2
        startRow=1
        startCol=2
        endCol=18
        targetCol=1
        daysForward= 1
        daysBackward = 45
        numNodes=0
        numDataPoints = w
        
        a = trainMulti(ticker, window, startRow, startCol, endCol, targetCol, numDataPoints, daysForward, daysBackward, numNodes)
        predictions.append(a[0])
        percent.append(a[1])
        error.append(a[2])
    print error
        
    print predictions
    print percent
    print average(error)
#    plt.plot(predictions,"g-")
#    plt.show()
#    plt.plot(percent,"b-")
#    plt.show()
    plt.plot(error,"r-")
    plt.show()
    
    timeFF = time.time()
    final_time = timeFF - timeS
    print "----------"+str(final_time)+"------------"

    
    print "done"