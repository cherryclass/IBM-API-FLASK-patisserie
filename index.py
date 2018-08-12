import os
import json
from flask import Flask
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'patisserie'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bonjour")
def bonjour():
    return "Bonjour"

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/gateau') 
def data(): 
	id = request.args.get('id')
	nom = request.args.get('nom')
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('insert into gateau values('+id+',"'+nom+'")')
	data = cursor.fetchall()
	if len(data) is 0:
		return json.dumps({'message':'gateau created successfully !'})
	else:
		return json.dumps({'error':str(data[0])})
	conn.close()

@app.route('/gateaux') 
def data2(): 
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('select * from gateau')
	data = cursor.fetchall()
	if len(data) != 0:
		return jsonify(data)
	else:
		return json.dumps({'error':str(data[0])})
	conn.close()

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
