from db import db
from constants import URL_PROJET
from typing import Dict, List, Union
ArticleJSON = Dict[str, Union[int, str, float]]

class ArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Text())
    titre = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text())
    # users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=False)
    cat_article_id = db.Column(db.Integer, db.ForeignKey('categorie_article.id'),
                            nullable=False)

    def __init__(self,titre,description,cat_id,photo):
        self.titre = titre 
        self.description = description
        self.cat_article_id = cat_id
        self.photo = photo

    def json(self) -> ArticleJSON:
        return {
            'id':self.id,
            'titre': self.titre,
            'description':self.description,
            'photo': URL_PROJET.format(self.photo),
            # 'user_id': self.users_id,
            'cat_article_id' : self.cat_article_id,
        }
    
    @classmethod
    def find_by_name(cls, titre: str) -> "ArticleModel":
        return cls.query.filter_by(titre=titre).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
    
    @classmethod
    def find_all(cls) -> List["ArticleModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None :
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()