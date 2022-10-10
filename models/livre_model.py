from db import db
from typing import Dict, List, Union
LivreJSON = Dict[str, Union[int, str, float]]
from constants import URL_PROJET



class LivreModel(db.Model):

    __tablename__ = 'livres'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80))
    lien_achat = db.Column(db.Text())
    photo = db.Column(db.Text())
    description = db.Column(db.Text())
    # users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=True)

    def __init__(self,titre:str,description:str,lien_achat:str,photo:str):
        self.titre = titre
        self.photo = photo
        self.description = description
        self.lien_achat = lien_achat

    
    @classmethod
    def find_by_id(cls, _id:int) -> "LivreModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> LivreJSON:
        return {
            'id':self.id,
            'titre': self.titre,
            'lien_achat': self.lien_achat,
            'photo':URL_PROJET.format(self.photo)
            # 'user_id': self.users_id,
        }

    @classmethod
    def find_by_name(cls, titre):
        return cls.query.filter_by(titre = titre).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()