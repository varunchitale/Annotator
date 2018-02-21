import json
import psycopg2
from flask import Flask,request
from flask import jsonify
import traceback
#import os
from flask_cors import CORS

conn = ''
def connectToDB():
        global conn
	try:

		params = json.load(open('DBSettings.json'))
		print "Connecting to database\n	->%s" %(params['dbname'])

		conn = psycopg2.connect(**params)
		print "Connected!\n"

		return conn
	except:
		print "Connection couldn't be established"

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
	return "Hello, World!<br>Proceed to /getdata?input=fileid for annotations"

@app.route('/getlines', methods=['GET','POST'])
def getdata():
	global conn
	#Check if connection is established	
	try:
		cursor = conn.cursor()
	except:
		conn = connectToDB()
		cursor = conn.cursor()


	
	try:
		fileid = request.args.get('input')
		query1 = "SELECT lines::json FROM analytics.file WHERE fileid = %s limit 1"
		cursor.execute(query1,[fileid])
	
		output = cursor.fetchone()


		return json.dumps(output[0])

	except:
		return 'Error'
		cursor = conn.cursor()


@app.route('/getsentences', methods=['GET','POST'])
def getsentences():
	global conn
	#Check if connection is established	
	try:
		cursor = conn.cursor()
	except:
		conn = connectToDB()
		cursor = conn.cursor()


	
	try:
		fileid = request.args.get('input')
		query1 = "SELECT sentences::json FROM analytics.file WHERE fileid = %s limit 1"
		cursor.execute(query1,[fileid])
	
		output = cursor.fetchone()


		return json.dumps(output[0])

	except:
		return 'Error: '
		cursor = conn.cursor()

if __name__ == '__main__':
	app.run(debug=True, host = '127.0.0.1', port = 8000)
	#app.run(debug=True, host = '127.0.0.1', port = 5555)
