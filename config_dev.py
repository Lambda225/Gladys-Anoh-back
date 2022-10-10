import os

basedire = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedire,'data.sqlite')
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/flask_app'
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = "kuckuebcqecize"
UPLOADED_IMAGES_DEST = os.path.join("static", "images")