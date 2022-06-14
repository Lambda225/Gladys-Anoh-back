from typing import Dict, List, Union
RoleJSON = Dict[str, Union[int, str, float]]
from db import db

class RoleModel(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
     # permet de definir une list d'éléments (lazy=dynamique)
    
    
    def __init__(self, name:str):
        self.name = name

    
    @classmethod
    def find_by_name(cls, name:str) -> "RoleModel":
        return cls.query.filter_by(name=name).first() # du au faites que nous avons supprimé la méthode init on doit passer
    #un keyword argument car notre class hérite de db.model qui permet cette modif
    def json(self) -> RoleJSON:
        return {
            'id':self.id,
            'name': self.name,
        }
    @classmethod
    def find_all(cls) -> List["RoleModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()