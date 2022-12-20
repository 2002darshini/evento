# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)
@app.route('/')
def option():
    return render_template("option.html")

@app.route('/College')
def College():
    return render_template("login.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'college' in request.form and 'id' in request.form and 'username' in request.form and 'password' in request.form:
		college = request.form['college']
		id = request.form['id']
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE college = % s AND username = % s AND password = % s', (college, username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			# cursor.execute("SELECT eventss.slno,eventss.event_name,eventss.event_type,eventss.start_date,eventss.end_date,eventss.fee FROM eventss,accounts where accounts.id=%s",(id,))
			# data= cursor.fetchall()
			# cursor.close()
			return render_template('index2.html')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'college' in request.form and 'id' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		college = request.form['college']
		id = request.form['id']
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not college or not id or not username or not password or not email:
			msg = 'Please fill out the form !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (%s, % s, % s, % s, % s)', (college, id, username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			return render_template('login.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

# @app.route('/eventConfirm')
# def eventConfirm():	
# 	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 	cursor.execute('SELECT * FROM eventss')
# 	result = cursor.fetchall()
# 	cursor.close()
# 	return render_template('eventConfirm.html',eventss=result)

# @app.route('/colgDetails/<string:id_no>', methods =['GET', 'POST'])
# def colgDetails(id_no):
# 	msg = ''
# 	if request.method == 'POST' and 'id' in request.form and 'event_type' in request.form and 'event_name' in request.form and 'desc' in request.form and 'start_date' in request.form and 'end_date' in request.form and 'fee' in request.form:
# 		# college = request.form['college']
# 		# id = request.form['id']
# 		event_type = request.form['event_type']
# 		event_name = request.form['event_name']
# 		# desc= request.form['desc']
# 		start_date = request.form['start_date']
# 		end_date=request.form['end_date']
# 		fee= request.form['fee']
# 		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 		cursor.execute('SELECT * FROM eventss WHERE id = % s', (id_no, ))
# 		event = cursor.fetchall()
# 		# if event:
# 		# 	msg = 'Event already exists !'
# 		if not event_type or not event_name or not start_date or not end_date or not fee or not id :
# 			msg = 'Please fill out the form !'
# 		else:
# 			cursor.execute('INSERT INTO eventss VALUES (% s, % s, % s, % s,% s)', ( event_type, event_name,start_date,end_date,fee, ))
# 			mysql.connection.commit()
# 			msg = 'Event added successfully !'
# 			return render_template('index.html')
# 	elif request.method == 'POST':
# 		msg = 'Please fill out the form !'
# 	return render_template('colgDetails.html', msg = msg)


@app.route('/index2')
def index2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT slno,event_name,event_type,start_date,end_date,fee,description FROM eventss")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', eventss=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        # slno = request.form['slno']
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        description = request.form['description']
        start_date= request.form['start_date']
        end_date= request.form['end_date']
        fee= request.form['fee']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO eventss (event_name, event_type, start_date,end_date,fee,description) VALUES (%s, %s,%s, %s, %s,%s)", (  event_name, event_type, start_date,end_date,fee,description))
        mysql.connection.commit()
        return redirect(url_for('index2'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM eventss WHERE slno=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index2'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        slno = request.form['slno']
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        description = request.form['description']
        start_date= request.form['start_date']
        end_date= request.form['end_date']
        fee= request.form['fee']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE eventss
               SET event_name=%s, event_type=%s, start_date=%s, end_date=%s, fee=%s,description=%s
               WHERE slno=%s
            """, (event_name, event_type,start_date,end_date,fee,description,slno))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index2'))

import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


#app = Flask(__name__)
#app.static_folder = 'static'

#@app.route("/")
#def home():
 #  return render_template("studentBase.html")
@app.route('/Student')
def Student():
   return render_template("studentBase.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


#if __name__ == "__main__":
    #app.run()



@app.route('/Hackathon')
def Hackathon():	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM eventss where event_type="Hackathon"')
	result = cursor.fetchall()
	cursor.close()
	return render_template('studSecond.html',eventss=result)

@app.route('/Workshop')
def Workshop():	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM eventss where event_type="Workshop"')
	result = cursor.fetchall()
	cursor.close()
	return render_template('studSecond.html',eventss=result)

@app.route('/Sports')
def Sports():	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM eventss where event_type="Sports"')
	result = cursor.fetchall()
	cursor.close()
	return render_template('studSecond.html',eventss=result)

@app.route('/Cultural')
def Cultural():	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM eventss where event_type="Cultural"')
	result = cursor.fetchall()
	cursor.close()
	return render_template('studSecond.html',eventss=result)

@app.route('/Seminar')
def Seminar():	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM eventss where event_type="Seminar"')
	result = cursor.fetchall()
	cursor.close()
	return render_template('studSecond.html',eventss=result)