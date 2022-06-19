from db import db
from typing import Dict, List, Union
PoscastJSON = Dict[str, Union[int, str, float]]


class PodcastModel(db.Model):

    __tablename__ = 'podcasts'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80))
    lien_achat = db.Column(db.Text())
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=True)

    @classmethod
    def find_by_email(cls, email:str) -> "PodcastModel":
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "PodcastModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> PoscastJSON:
        return {
            'id':self.id,
            'titre': self.titre,
            'lien_achat': self.lien_achat,
            'user_id': self.users_id,
        }
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()