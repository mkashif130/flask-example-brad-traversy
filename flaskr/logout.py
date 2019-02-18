from flask import Flask, flash, redirect, url_for, session, logging, request,current_app,Blueprint
from flask_mysqldb import MySQL

#Creating blue print, This is used in __init__.py
blueprint = Blueprint('logout',__name__,url_prefix='/logout')

#logout
@blueprint.route('/')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login.login'))
