import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR

dates = []
Time = []

def get_data(filename):
	with open(filename,'r') as csvfile:
		csvFileReader = csv.reader(csvfile)
		next(csvFileReader)
		for row in csvFileReader:
			day=int(row[0].split('-')[0])
			month=int(row[0].split('-')[1])
			dates.append(int(day+(month-1)*30))
			Time.append(float(row[1]))
	return 

def predict_Time(dates,Time,x):
	dates=np.reshape(dates,(len(dates),1))
	#svr_lin = SVR(kernel='linear',C=1e3)
	svr_poly = SVR(kernel='poly',C=1e2,degree=2)
	#svr_rbf = SVR(kernel='rbf',C=1e3,gamma=0.1)
	#svr_lin.fit(dates,Time)
	svr_poly.fit(dates,Time)
	#svr_rbf.fit(dates,Time)

	plt.scatter(dates,Time,color='black',label='Data')
	#plt.plot(dates,svr_rbf.predict(dates),color='red',label='RBF model')
	#plt.plot(dates,svr_lin.predict(dates),color='green',label='Linear model')
	plt.plot(dates,svr_poly.predict(dates),color='blue',label='Polynomial model')
	plt.xlabel('Days')
	plt.ylabel('Estimated Time')
	plt.title('SVR')
	plt.legend()
	plt.show()

	#return svr_rbf.predict(x)[0]
	#return svr_lin.predict(x)[0]
	svr_poly.predict(x)[0]

get_data('datasec.csv')
predicted_time=predict_Time(dates,Time,201)
print abs(predicted_time)