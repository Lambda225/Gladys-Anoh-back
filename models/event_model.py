from email.policy import default
from db import db
from typing import Dict, List, Union
import datetime
from constants import URL_PROJET
EventJSON = Dict[str, Union[int, str, float]]
from models.billet_model import BilletModel

class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), unique=True)
    cout = db.Column(db.Integer)
    date = db.Column(db.String(80), unique=True)
    presentiel = db.Column(db.Boolean, default=True)
    photo = db.Column(db.Text())
    nom_de_place = db.Column(db.Integer)
    description = db.Column(db.Text())
    # billet = db.relationship('BilletModel', backref='events', lazy=True)
    # avis = db.relationship('AvisModel', backref='events', lazy=True)

    def __init__(self, titre:str, date:str, presentiel:bool, cout:float, nom_de_place:int, description:str,photo:str):
        self.titre          = titre
        self.photo          = photo
        self.cout           = cout
        self.date           = date
        self.presentiel     = presentiel
        self.nom_de_place   = nom_de_place
        self.description    = description
        

    def json(self) -> EventJSON:
        return {
            'id':self.id,
            'titre': self.titre,
            'photo': URL_PROJET.format(self.photo),
            'cout': self.cout,
            'date':self.date,
            'nom_de_place':self.nom_de_place,
            'description':self.description,
            # 'billets': [billet.id for billet in self.billet ],
            # 'avis': [avi.id for avi in self.avis],
        }

    @classmethod
    def find_by_name(cls, titre: str) -> "EventModel":
        return cls.query.filter_by(titre=titre).first()
    
    @classmethod
    def find_all(cls) -> List["EventModel"]:
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