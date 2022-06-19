from db import db
from typing import Dict, List, Union
AvisJSON = Dict[str, Union[int, str, float]]

class AvisModel(db.Model):

    __tablename__ = 'avis'

    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text())
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'),
                            nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=True)

    def __init__(self,titre:str,contenu:str):
        self.titre = titre
        self.contenu = contenu

    def json(self) -> AvisJSON:
        return {
            'id':self.id,
            'contenu': self.contenu,
            'event_id':self.event_id,
            'user_id': self.users_id,
        }
    
    @classmethod
    def find_by_name(cls, titre: str) -> "AvisModel":
        return cls.query.filter_by(titre=titre).first()
    
    @classmethod
    def find_all(cls) -> List["AvisModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None :
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()