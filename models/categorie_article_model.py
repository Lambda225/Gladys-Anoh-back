from db import db
from typing import Dict, List, Union
CatArticleJSON = Dict[str, Union[int, str, float]]
from models.article_model import ArticleModel

class CatArticleModel(db.Model):

    __tablename__ = 'categorie_article'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    articles = db.relationship('ArticleModel', backref='categorie_article', lazy=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=False)
    
    def __init__(self,titre:str,description:str):
        self.titre = titre
        self.description = description
        
    def json(self) -> CatArticleJSON:
        return {
            'id':self.id,
            'description': self.description,
            'articles' : [article.id for article in self.articles],
            'user_id': self.users_id,
        }
    
    @classmethod
    def find_by_name(cls, titre: str) -> "CatArticleModel":
        return cls.query.filter_by(titre=titre).first()
    
    @classmethod
    def find_all(cls) -> List["CatArticleModel"]:
        return cls.query.all()