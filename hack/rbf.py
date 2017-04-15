import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
People = []
Time = []


def get_data(filename):
	with open(filename,'r') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)
		for row in csvFileReader:
			People.append(int(row[0]))
			Time.append(float(row[1]))
	return 

def predict_Time(People,Time,x):
	People=np.reshape(People,(len(People),1))
	#svr_lin = SVR(kernel='linear',C=1e3)
	#svr_poly = SVR(kernel='poly',C=1e3,degree=2)
	svr_rbf = SVR(kernel='rbf',C=1e3,gamma=0.1)
	#svr_lin.fit(People,Time)
	#svr_poly.fit(People,Time)
	svr_rbf.fit(People,Time)

	#plt.scatter(People,Time,color='black',label='Data')
	#plt.plot(People,svr_rbf.predict(People),color='red',label='RBF model')
	#plt.plot(People,svr_lin.predict(People),color='green',label='Linear model')
	#plt.plot(People,svr_poly.predict(People),color='blue',label='Polynomial model')
	
	#plt.xlabel('People')
	#plt.ylabel('Estimated Time')
	#plt.title('SVR')
	#plt.legend()
	#plt.show()
	
	return svr_rbf.predict(x)[0]
	#,svr_lin.predict(x)[0],svr_poly.predict(x)[0]
#get_data('datasec.csv')
get_data('datasec.csv')	
predicted_time=predict_Time(People,Time,len(People))
predicted_time=abs(predicted_time)

num_lines = sum(1 for line in open('datasec.csv'))
with open("datasec.csv", "a") as f:
    f.write(str(num_lines)+','+str(predicted_time) + '\n')
print predicted_time
	#print People,Time
#print abs(predicted_time)
