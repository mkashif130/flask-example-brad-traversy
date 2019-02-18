from flask import Blueprint,render_template

blueprint = Blueprint('home',__name__,url_prefix='/')

@blueprint.route('/')
def index():
	return render_template('home.html')
