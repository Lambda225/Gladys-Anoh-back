from db import db
from typing import Dict, List, Union
BilletJSON = Dict[str, Union[int, str, float]]



class BilletModel(db.Model):

    __tablename__ = 'billets'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), unique=True)
    lien_session = db.Column(db.Text(), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'),
                            nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=True)
                            
    def __init__(self,titre:str,description:str,lien_session:str):
        self.titre = titre
        self.lien_session = lien_session
        self.description = description


    @classmethod
    def find_by_email(cls, email:str) -> "BilletModel":
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "BilletModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> BilletJSON:
        return {
            'id':self.id,
            'titre': self.titre,
            'lien_session': self.lien_session,
            'event.id':self.event_id,
            'user.id':self.user_id
        }
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()