from flask import Blueprint,render_template, current_app, url_for, session, logging, request,flash,redirect
from flask_mysqldb import MySQL
from functools import wraps
from wtforms import  Form, StringField, TextAreaField, PasswordField, validators

#Creating blue print, This is used in __init__.py
blueprint = Blueprint('articles',__name__,url_prefix='/articles')

#Article Add edit
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=250)])
	body =TextAreaField('Body', [validators.Length(min=30)])



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


#root path under articles
@blueprint.route('/')
def articles():
	#app_context can only be access during request
	mysql =current_app.config["MY_SQL"]
	#Create cursor
	cur = mysql.connection.cursor()

	#Get articles
	result = cur.execute("Select * from Articles")
	articles = cur.fetchall()

	if result > 0:
		return render_template('articles.html', articles =  articles)
	else:
		msg = 'No Article Found'
		return render_template('articles.html', msg = msg)

	#Close Connection
	cur.close()

#View one article
@blueprint.route('article/<string:id>/')
def article(id):
	#app_context can only be access during request
	mysql =current_app.config["MY_SQL"]

	#Cursor
	cur = mysql.connection.cursor()

	#Get Article
	result = cur.execute("select * from Articles where id = %s", [id])
	article =  cur.fetchone()
	cur.close()
	return render_template('article.html', article=article)


@blueprint.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):

	#app_context can only be access during request
	mysql =current_app.config["MY_SQL"]

	#Cursor
	cur = mysql.connection.cursor()

	#execute
	cur.execute("delete from articles where id = %s", [id])

	#commit
	mysql.connection.commit()

	#Close
	cur.close()

	flash("Article deleted",'success')
	return redirect(url_for('dashboard.dashboard'))

@blueprint.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
	#app_context can only be access during request
	mysql =current_app.config["MY_SQL"]

	#cursor
	cur =mysql.connection.cursor()

	#Get
	result = cur.execute("select * from articles where id=%s",[id])
	article = cur.fetchone()

	#Get form
	form = ArticleForm(request.form)

	#populate form fields
	form.title.data = article['title']
	form.body.data = article['body']

	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']

		#cursor
		cur = mysql.connection.cursor()

		#execute
		cur.execute("Update articles set title = %s, body =%s where id = %s", (title,body,id) )

		#commit
		mysql.connection.commit()

		#close
		cur.close()

		flash("Article Updated successfully", "success")
		return redirect(url_for('dashboard.dashboard'))

	return render_template('edit_article.html', form=form)

@blueprint.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	#app_context can only be access during request
	mysql =current_app.config["MY_SQL"]

	form = ArticleForm(request.form)
	if request.method=='POST' and form.validate():
		title = form.title.data
		body = form.body.data

		#cursor
		cur = mysql.connection.cursor()

		#execute
		cur.execute("insert into articles(title,body,author) Values(%s,%s,%s)",(title,body,session['username']))

		#commit
		mysql.connection.commit()

		#close
		cur.close()
		flash("Article Created",'success')
		return redirect(url_for('dashboard.dashboard'))

	return render_template('add_article.html',form=form)
