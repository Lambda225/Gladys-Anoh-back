from flask_restful import Resource
from models.store_model import StoreModel
from flask_jwt_extended import jwt_required
from constants import *

class Store(Resource):
    @classmethod
    def get(cls, name:str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': NOT_FOUND.format("store")}, 404
    
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name:str):
        if StoreModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXIST.format("store", name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': ERROR_INSERTING.format("store")}, 500
        return store.json(), 201

    @classmethod
    def delete(cls, name:str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': DELETED.format("store")}

class StoreList(Resource):
    @classmethod
    def get(cls):
        return {'stores': [store.json() for store in StoreModel.query.all()]}