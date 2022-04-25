import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Definition de chemin vers le app.py
basedire = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blablayzcyzq'

#configue de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedire,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#Instanciation de SQLALCHEMY
db = SQLAlchemy(app)
Migrate(app, db)

#initialisation des blueprints
from blueprints.user.views import user

app.register_blueprint(user,url_prefix='/user')