from db import db
from typing import Dict, List, Union
CatPodcsaJSON = Dict[str, Union[int, str, float]]
from models.posdcast_model import PodcastModel

class CatPodcsatModel(db.Model):

    __tablename__ = 'categorie_podcast'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    podcasts = db.relationship('PodcastModel', backref='categorie_podcast', lazy=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=False)
    
    def __init__(self,titre:str,description:str):
        self.titre = titre
        self.description = description
        
    def json(self) -> CatPodcsaJSON:
        return {
            'id':self.id,
            'description': self.description,
            'podcasts' : [podcast.id for podcast in self.podcasts],
            'user_id': self.users_id,
        }
    
    @classmethod
    def find_by_name(cls, titre: str) -> "CatPodcsatModel":
        return cls.query.filter_by(titre=titre).first()
    
    @classmethod
    def find_all(cls) -> List["CatPodcsatModel"]:
        return cls.query.all()