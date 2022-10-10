from db import db
from typing import Dict, List, Union
QuestionJSON = Dict[str, Union[int, str, float]]

class QuestionModel(db.Model):

    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text())
    reponse_id = db.Column(db.Integer, db.ForeignKey('reponse.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=True)

    def __init__(self,contenu):
        self.contenu = contenu
        
    @classmethod
    def find_by_name(cls, contenu:str) -> "QuestionModel":
        return cls.query.filter_by(contenu = contenu).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "QuestionModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> QuestionJSON:
        return {
            'id':self.id,
            'contenu': self.contenu,
            'reponse_id':self.reponse_id,
            # 'user_id':self.user_id,
        }
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()
