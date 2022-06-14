from typing import Dict, List

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import  jwt_required, get_jwt
from models.roles_model import RoleModel
from constants import *


class Role(Resource):

    @classmethod
    def get(cls, name:str):
        role = RoleModel.find_by_name(name)
        if role:
            return role.json()
        return {'message': 'role not found'}, 404

    @classmethod
    # @jwt_required()
    def post(cls, name:str):
        if RoleModel.find_by_name(name):
            return {"message":NAME_ALREADY_EXIST.format(name, 'role')}, 400
        role = RoleModel(name)
        try:
            role.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format('role')}, 500
        return role.json(), 201

    @classmethod
    # @jwt_required()
    def delete(cls, name:str):
        role = RoleModel.find_by_name(name)
        if role:
            role.delete_from_db()
            return {'message': DELETED.format('role')}
        return {'message': NOT_FOUND.format("role")}, 404

    @classmethod
    def put(cls, name:str):
        role = RoleModel.find_by_name(name)
        if role is None:
            role = RoleModel(name)
        else:
            role.name = name
        role.save_to_db()
        return role.json()


class RoleList(Resource):
    @classmethod
    def get(cls):
        return {'roles': [role.json() for role in RoleModel.query.all()]}, 200
