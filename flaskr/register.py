from flask import Flask, render_template, flash, redirect, url_for, session, logging, request,current_app,Blueprint
from flask_mysqldb import MySQL
from wtforms import  Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


#Creating blue print, This is used in __init__.py
blueprint = Blueprint('register',__name__,url_prefix='/register')


class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username =StringField('Username', [validators.Length(min=4, max=50)])
	email =StringField('Email', [validators.Email()])
	password =PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

@blueprint.route('/', methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method=='POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#app_context can only be access during request
		mysql =current_app.config["MY_SQL"]

		#create Cusros
		cur = mysql.connection.cursor()

		cur.execute("Insert into Users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))

		#commit to # DEBUG:
		mysql.connection.commit()

		#close the connection
		cur.close()

		flash("You are now registered and can login","success")
		return redirect(url_for('login.login'))
	return render_template('register.html', form=form)
