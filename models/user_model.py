from email.policy import default
from db import db
from flask import request, url_for
from requests import Response
from libs.mailgun import Mailgun


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    profession = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    
    @classmethod
    def find_by_email(cls, email:str) -> "UserModel":
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "UserModel":
        return cls.query.filter_by(id = _id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()