import random
import time
import MultiNode
import matplotlib.pyplot as plt
from multiprocessing import Pool
from numpy import average
random.seed()


def Multi(N):
    ticker="LUVBBF3"
    window= 100
    startRow=1
    startCol=2
    endCol=33
    targetCol=1
    daysForward= N+1
    daysBackward = N
    numNodes=window
    numDataPoints=1700-window
        
    return MultiNode.trainMulti(ticker, window, startRow, startCol, endCol, targetCol, numDataPoints, daysForward, daysBackward, numNodes)


if __name__ == '__main__':
    
    startTime = time.time()
    timeS = time.time()
    
    daysF = 10
    N = []
    predictions= []
    percent = []
    error = []
    yBack = []
    for x in range(1,daysF+1):
        N.append(x)
        
     
    #create a process Pool with 4 processes
    pool = Pool(processes=10)
     
    #map doWork to availble Pool processes
    results = pool.map(Multi,N)
    
    endTime = time.time()
    
    #sum the partial results to get the final result
    total_time = endTime-startTime
    print results
    print total_time
    
    for a in range(len(results)):
        predictions.append(results[a][0])
        percent.append(results[a][1])
        error.append(results[a][2])
    yBack.append(results[a][3])
    
    plt.plot(yBack[0][0],"g-")
    plt.plot(predictions, "b--")
    plt.show()
    
    timeFF = time.time()
    final_time = timeFF - timeS
    print "----------"+str(final_time)+"------------"
    print predictions
    print percent
    print error
    
    ERROR = []
    for x in range(len(predictions)):
        ERROR.append((yBack[0][0][x]-predictions[x])/abs(yBack[0][0][x]))
        
    print average(ERROR), "45 DAY ERROR"
    plt.plot(ERROR, "r-")
    plt.show()  
    
    
#    sound =  "C:\Users\Luke Farrell\Desktop\Notorious BIG ft P.Diddy & Mase-Mo Money Mo Problems-w lyrics.wav"
#   
#    sound2 = winsound.PlaySound(sound, winsound.SND_FILENAME)
#    
#    print "done"