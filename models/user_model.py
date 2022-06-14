from json import dump
from typing import List
from typing import Dict, List, Union

from sqlalchemy import JSON
UserJSON = Dict[str, Union[int, str, float]]
from email.policy import default
from db import db
from flask import request, url_for
from requests import Response
from models.user_role_model import association_table



class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    profession = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80))
    roles = db.relationship('RoleModel',
                               secondary=association_table, backref="userslist")
    
    
    
    @classmethod
    def find_by_email(cls, email:str) -> "UserModel":
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def find_by_id(cls, _id:int) -> "UserModel":
        return cls.query.filter_by(id = _id).first()
    
    def json(self) -> UserJSON:
        return {
            'id':self.id,
            'nom': self.nom,
            'profession': self.profession,
            'email': self.email,
            'roles': [role.name for role in self.roles ],
            'naissance':self.birthday
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self)  -> None:
        db.session.delete(self)
        db.session.commit()