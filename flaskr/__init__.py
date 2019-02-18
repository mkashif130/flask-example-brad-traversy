import os
from flask import Flask
from flask_mysqldb import MySQL
from . import home, about, articles, register,login,dashboard,logout

def create_app(test_config=None):
	#Create flask application
	app=Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY="dev",
		MYSQL_HOST = "localhost",
		MYSQL_USER = "root",
		MYSQL_PASSWORD = "admin",
		MYSQL_DB = "flaskexample",
		MYSQL_CURSORCLASS = "DictCursor",
		DEBUG = True
	)
	mysql =MySQL(app)
	app.config["MY_SQL"] = mysql
	app.app_context().push()

	app.register_blueprint(home.blueprint)
	app.register_blueprint(about.blueprint)
	app.register_blueprint(articles.blueprint)
	app.register_blueprint(register.blueprint)
	app.register_blueprint(login.blueprint)
	app.register_blueprint(dashboard.blueprint)
	app.register_blueprint(logout.blueprint)

	return app
