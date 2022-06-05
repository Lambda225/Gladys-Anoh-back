from flask_restful import Resource, reqparse
from models.user_model import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from blocklist import BLOCKLIST
from constants import *

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True,
                            help=BLANK_ERROR.format("username"))
_user_parser.add_argument('password', type=str, required=True,
                            help=BLANK_ERROR.format("password"))

class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":NAME_ALREADY_EXIST.format("user", data['username'])}, 400
        user = UserModel(**data)
        user.save_to_db()

        return  {"message": CREATED.format("user")}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': NOT_FOUND.format("user")}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': NOT_FOUND.format("user")}, 404
        user.delete_from_db()
        return {'message':DELETED.format("user")}, 200 
    
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity = user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token':access_token, 'refresh_token': refresh_token}, 200
        return {'message':INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti'] #identifiant unique jwt
        BLOCKLIST.add(jti)
        return {'message': LOGGED_OUT}, 200