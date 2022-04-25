from flask import Blueprint,render_template, url_for, request , redirect,session,Response,request

user = Blueprint('user',__name__,template_folder='templates',static_folder='static')

@user.route('/')
def home():
    return render_template('home.html')

@user.route('/formation')
def formation():
    return render_template('formation.html')

@user.route('/livre')
def livre():
    return render_template('livre.html')

@user.route('/podcast')
def podcast():
    return render_template('podcast.html')

@user.route('/apropos')
def apropos():
    return render_template('apropos.html')