from flask import Flask, render_template, flash, redirect, url_for, session, logging, request,current_app,Blueprint
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps


#Creating blue print, This is used in __init__.py
blueprint = Blueprint('dashboard',__name__,url_prefix='/dashboard')

#unauthorized check
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('unauthorized access','danger')
			return redirect(url_for('login.login'))
	return wrap


#dashboard
@blueprint.route('/')
@is_logged_in
def dashboard():
	#app_context can only be access during request
	mysql =current_app.config["MY_SQL"]

	#Create cursor
	cur = mysql.connection.cursor()

	#Get articles
	result = cur.execute("Select * from Articles")
	articles = cur.fetchall()

	if result > 0:
		return render_template('dashboard.html', articles =  articles)
	else:
		msg = 'No Article Found'
		return render_template('dashboard.html', msg = msg)

	#Close Connection
	cur.close()
