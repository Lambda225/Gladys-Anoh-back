from db import db
from typing import Dict, List, Union
CatArticleJSON = Dict[str, Union[int, str, float]]
from models.article_model import ArticleModel
from constants import URL_PROJET

class CatArticleModel(db.Model):

    __tablename__ = 'categorie_article'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80))
    description = db.Column(db.Text())
    articles = db.relationship('ArticleModel', backref='categorie_article', lazy=True,cascade="all, delete-orphan")
    photo = db.Column(db.Text())
    # users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=False)
    
    def __init__(self,titre,description,photo):
        self.titre = titre
        self.photo = photo
        self.description = description
        
    def json(self) -> CatArticleJSON:
        return {
            'id':self.id,
            'titre':self.titre,
            'description': self.description,
            'photo':URL_PROJET.format(self.photo),
            'articles' : [article.id for article in self.articles],
            # 'user_id': self.users_id,
        }
    
    @classmethod
    def find_by_name(cls, titre):
        return cls.query.filter_by(titre = titre).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()


    def save_to_db(self) -> None :
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()