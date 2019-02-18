from flask import Flask, render_template, flash, redirect, url_for, session, logging, request,current_app,Blueprint
from flask_mysqldb import MySQL
from wtforms import  Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


#Creating blue print, This is used in __init__.py
blueprint = Blueprint('login',__name__,url_prefix='/login')


@blueprint.route('/', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		#app_context can only be access during request
		mysql =current_app.config["MY_SQL"]

		#Get forms fiels
		username = request.form['username']
		password_candidate = request.form['password']

		#Create a cursor
		cur = mysql.connection.cursor();

		#get user by Username
		result =  cur.execute("select * from users where username=%s;",[username])

		if result > 0:
			#Get stored hash
			data = cur.fetchone()
			password = data['password']

			#compare password_candidate
			if sha256_crypt.verify(password_candidate, password):
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard.dashboard'))
			else:
				error = 'invalid login'
				return render_template('login.html', error=error)
		else:
			error = 'username not found'
			return render_template('login.html', error=error)
		cur.close()
	return render_template('login.html')
