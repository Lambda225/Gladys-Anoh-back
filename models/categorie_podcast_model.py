from db import db
from typing import Dict, List, Union
CatPodcsaJSON = Dict[str, Union[int, str, float]]
from models.podcast_model import PodcastModel
from constants import URL_PROJET

class CatPodcastModel(db.Model):

    __tablename__ = 'categorie_podcast'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80))
    description = db.Column(db.Text())
    lienspotify = db.Column(db.Text())
    photo = db.Column(db.Text())
    podcasts = db.relationship('PodcastModel', backref='categorie_podcast', lazy=True,cascade="all, delete-orphan")
    # users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=False)
    
    def __init__(self,titre:str,description:str,lienspotify:str,photo):
        self.titre = titre
        self.photo = photo
        self.lienspotify = lienspotify
        self.description = description
        
    def json(self) -> CatPodcsaJSON:
        return {
            'id':self.id,
            'titre':self.titre,
            'lienspotify':self.lienspotify,
            'description': self.description,
            'photo': URL_PROJET.format(self.photo),
            'podcasts' : [podcast.id for podcast in self.podcasts],
            # 'user_id': self.users_id,
        }
    
    @classmethod
    def find_by_name(cls, titre: str) -> "CatPodcastModel":
        return cls.query.filter_by(titre=titre).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
    
    @classmethod
    def find_all(cls) -> List["CatPodcastModel"]:
        return cls.query.all()

    def save_to_db(self) -> None :
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()