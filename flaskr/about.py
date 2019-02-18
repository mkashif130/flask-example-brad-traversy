# from flask import Blueprint,render_template
#
# blueprint = Blueprint('about',__name__,url_prefix='/about')
#
# @blueprint.route('/about')
# def about():
# 	return render_template('about.html')

from flask import Blueprint,render_template

blueprint = Blueprint('about',__name__,url_prefix='/about')

@blueprint.route('/')
def index():
	return render_template('about.html')
