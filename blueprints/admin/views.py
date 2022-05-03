from flask import Blueprint,render_template, url_for, request , redirect,session,Response,request

admin = Blueprint('admin',__name__,template_folder='templates',static_folder='static')

@admin.route('/')
def home():
    return render_template('admin_home.html')