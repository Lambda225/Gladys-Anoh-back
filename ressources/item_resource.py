from typing import Dict, List

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import  jwt_required, get_jwt
from models.item_model import ItemModel
from constants import *


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help=BLANK_ERROR.format("price"))
    parser.add_argument('store_id', type=int, required=True,
                        help=BLANK_ERROR.format("store_id"))

    @classmethod
    def get(cls, name:str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    @classmethod
    @jwt_required()
    def post(cls, name:str):
        if ItemModel.find_by_name(name):
            return {"message":NAME_ALREADY_EXIST.format(name, 'item')}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format('item')}, 500
        return item.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name:str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': DELETED.format('item')}
        return {'message': NOT_FOUND.format("item")}, 404

    @classmethod
    def put(cls, name:str):
        data=Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
