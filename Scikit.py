'''
Created on Apr 15, 2016

@author: Jake Shulman
'''
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_ridge import KernelRidge
from sklearn import svm
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.qda import QDA
from sknn.mlp import Regressor,Layer
csv = np.genfromtxt ('fb.csv', delimiter=",")
openPrice = csv[:,1]
high = csv[:,2]
low  = csv[:,3]
close = csv[:,4]
volume = csv[:,5]
adjusted_close=csv[:,6]
print csv[-1][1]

length=len(high)
values=[openPrice,high,low,close,volume,adjusted_close]

N=100
Start=500
End=100
#from 1000->800...300->200 
#predict sum(200->today)/actual percent correct over 200 day period

w, h = 6, Start-End+1
X = [[0 for x in range(w)] for y in range(h)] 

# print X
# print values[0][7915]
# print values[0][7915+200]
# X[0][5]=values[0][8915-1000]-values[0][8915-1000+N]
# print X
for y in range(w):
    for x in range(Start,End,-1):
        X[x-101][y]=(values[y][length-x]-values[y][length-x+N])
a=csv[:,7]
y=a[length-Start-Start+End:length-Start+1]


 
scaler = StandardScaler()
scaler.fit(X)  
X_train = scaler.transform(X)
print X_train
print y
PercentCorrect=[]
exper=[]
# clf=linear_model.SGDRegressor()
# clf = KernelRidge(alpha=.001)
clf = svm.SVR(kernel="rbf")
# clf = linear_model.Lasso(alpha=2.5)
# clf = linear_model.BayesianRidge()
# clf = linear_model.LinearRegression()
# clf = linear_model.ARDRegression()
# clf = linear_model.ElasticNet()
# clf = linear_model.BayesianRidge()
# clf = linear_model.LassoLars(alpha=.1)
# clf = linear_model.RidgeCV()
# clf = linear_model.Ridge()
# clf = QDA()
# clf = svm.SVR()
clf.fit(X_train, y)
y_train=y
# clf= Regressor(
#     layers=[
#         Layer("Rectifier", units=100),
#         Layer("Linear")],
#     learning_rate=0.2,
#     n_iter=10)
# clf.fit(X_train, y_train)


for x in range(0,99):
    X_test=[openPrice[length-1-x]-openPrice[length-x-N],high[length-1-x]-high[length-x-N],low[length-1-x]-low[length-x-N],close[length-1-x]-close[length-x-N],volume[length-1-x]-volume[length-x-N],adjusted_close[length-1-x]-adjusted_close[length-x-N]]
    print type(X_test)
    X_test = scaler.transform(X_test)  # apply same transformation to test data

    PercentCorrect.append(((a[-(2+x)]-(clf.predict(X_test))[0]))/a[-(2+x)])
    exper.append(clf.predict(X_test))
count=0.0
# plt.plot(PercentCorrect)
print exper
plt.plot(exper)
plt.plot(a[length-100:length])
print(exper)
   
plt.show()
  
  
     
          
