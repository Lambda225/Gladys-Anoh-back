from re import S
from db import db
from typing import Dict, List, Union
from constants import URL_PROJET
PoscastJSON = Dict[str, Union[int, str, float]]


class PodcastModel(db.Model):

    __tablename__ = 'podcasts'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80))
    ifram = db.Column(db.Text())
    description = db.Column(db.Text())
    photo = db.Column(db.Text())
    # users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=False)
    cat_podcast_id = db.Column(db.Integer, db.ForeignKey('categorie_podcast.id'),
                            nullable=False)

    def __init__(self,titre:str,photo:str,description:str,ifram:str,cat_id:int):
        self.titre = titre
        self.photo = photo
        self.ifram = ifram
        self.cat_podcast_id = cat_id
        self.description = description

    @classmethod
    def find_by_name(cls, name:str) -> "PodcastModel":
        return cls.query.filter_by(titre = name).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "PodcastModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> PoscastJSON:
        return {
            'id':self.id,
            'titre': self.titre,
            'Ifram': self.ifram,
            'description':self.description,
            'photo':URL_PROJET.format(self.photo),
            # 'user_id': self.users_id,
            'cat_podcast_id' : self.cat_podcast_id,
        }

    @classmethod
    def find_by_name(cls, titre):
        return cls.query.filter_by(titre = titre).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()