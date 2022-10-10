from json import dump
from typing import List
from typing import Dict, List, Union

from sqlalchemy import JSON
UserJSON = Dict[str, Union[int, str, float]]
from email.policy import default
from db import db
from flask import request, url_for
from requests import Response
from models.user_role_model import association_table
from models.article_model import ArticleModel
from models.livre_model import LivreModel
from models.avis_model import AvisModel
from models.billet_model import BilletModel
from models.categorie_article_model import CatArticleModel
from models.categorie_podcast_model import CatPodcastModel
from models.question_model import QuestionModel
from models.reponse_model import ReponseModel


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    prenom = db.Column(db.String(80))
    profession = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80))
    roles = db.relationship('RoleModel',
                               secondary=association_table, backref="users")
    # articles = db.relationship('ArticleModel', backref='users', lazy=True)
    # livres = db.relationship('LivreModel', backref='users', lazy=True)
    # avis = db.relationship('AvisModel', backref='users', lazy=True)
    # billets = db.relationship('BilletModel', backref='users', lazy=True)
    # cat_articles = db.relationship('CatArticleModel', backref='users', lazy=True)
    # cat_podcasts = db.relationship('CatPodcastModel', backref='users', lazy=True)
    # questions = db.relationship('QuestionModel', backref='users', lazy=True)
    # reponses = db.relationship('ReponseModel', backref='users', lazy=True)

    
    
    
    @classmethod
    def find_by_email(cls, email:str) -> "UserModel":
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "UserModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> UserJSON:
        return {
            'id':self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'profession': self.profession,
            'email': self.email,
            'roles': [role.name for role in self.roles ],
            # 'articles': [article.id for article in self.articles],
            # 'livres': [livre.id for livre in self.livres],
            'naissance':self.birthday,
            # 'avis': [avi.id for avi in self.avis],
            # 'billets': [billet.id for billet in self.billets],
            # 'cat_articles' : [cat_article.id for cat_article in self.cat_articles],
            # 'questions': [question.id for question in self.questions],
            # 'reponses': [reponse.id for reponse in self.reponses]
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()