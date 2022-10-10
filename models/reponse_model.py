from db import db
from typing import Dict, List, Union
ReponseJSON = Dict[str, Union[int, str, float]]
from models.question_model import QuestionModel

class ReponseModel(db.Model):

    __tablename__ = 'reponse'
    
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text())
    questions = db.relationship('QuestionModel', backref='reponse', lazy=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    #                         nullable=True)
    
    def __init__(self,contenu:str):
        self.contenu = contenu
        
    @classmethod
    def find_by_name(cls, contenu:str) -> "ReponseModel":
        return cls.query.filter_by(contenu = contenu).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "ReponseModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> ReponseJSON:
        return {
            'id':self.id,
            'contenu': self.contenu,
            'questions': [question.id for question in self.questions],
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