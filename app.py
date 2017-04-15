from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import time
from functools import wraps
import sqlite3
from datetime import datetime
import urllib2, json
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
People = []
Time = []
READ_API_KEY = "55MVULVPSBETX9SQ"
CHANNEL_ID = "252109"



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

conn = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))

response = conn.read()
print "http status code=%s" % (conn.getcode())
data=json.loads(response)
lat = data['field1']
print "Total number of people in queue"
print lat

if(lat > 0):
	total_time = predicted_time*lat
	print "Total time in queue"
	print total_time

urllib2.urlopen("https://api.thingspeak.com/update?api_key=FB5AT91NHWIL8T5Q&field1=%s"%(total_time))

# Application object
app = Flask(__name__)
app.secret_key = "praveen"

db = SQLAlchemy(app)

# Sqlalchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#from db_create import *
#from models import Blogpost

# Login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrap


# Routes
@app.route('/login', methods=["GET", "POST"])
def login():
	error = None
	if(request.method=="POST"):
		if(request.form['username'] == "admin" and request.form['password'] == "jenny"):
			session['logged_in'] = True
			return redirect(url_for('home'))

		else:
			error = "Invalid Credentials!!!"
	return render_template("login.html", error=error)

@app.route('/gate', methods=["GET", "POST"])
def gate():
  
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			print "SUBMIT"
			To = request.form['To']
			From = request.form['From']
			fn = request.form['Flightno']
			print To, From, fn
			urllib2.urlopen("https://api.thingspeak.com/update?api_key=LHBZ7SHGDQXF953F&field1=%s"%(To))
			urllib2.urlopen("https://api.thingspeak.com/update?api_key=D6JIG8SWZECBF1KN&field1=%s"%(From))
			urllib2.urlopen("https://api.thingspeak.com/update?api_key=16OWYKZHUIMEYURI&field1=%s"%(fn) )
	return render_template("gatechange.html")

@app.route('/home', methods=["GET", "POST"])
def home():
	
	if request.method == 'POST':
		if request.form['submit'] == 'Next':
			print "happening"
			return(redirect(url_for('gate')))
	return render_template("index.html")

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)

