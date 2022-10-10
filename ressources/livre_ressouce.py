import os
from flask_restful import Resource, reqparse
from models.livre_model import LivreModel
import werkzeug
import uuid
from flask_jwt_extended import jwt_required, get_jwt
from constants import * 
from libs.image_helper import get_extension,get_path,save_image

_livre_parser = reqparse.RequestParser()
_livre_parser.add_argument('titre', type=str,location='form', required=True,
                            help=BLANK_ERROR.format("titre"))
_livre_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',required=True,
                                help=BLANK_ERROR.format('photo') )
_livre_parser.add_argument('lien_achat', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("lien_achat"))
_livre_parser.add_argument('description', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("description"))

_livre_put_parser = _livre_parser.copy()
_livre_put_parser.remove_argument('photo')
_livre_put_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',
                                help=BLANK_ERROR.format('photo') )

class LivreRegister(Resource):
    @classmethod
    # @jwt_required()
    def post(cls):
        data = _livre_parser.parse_args() 
        # jti = get_jwt()['jti'] #identifiant unique jwt
        # print(jti)
        if LivreModel.find_by_name(data['titre']):
            return {'message' : NAME_ALREADY_EXIST.format('Livre', data['titre'])}, 400

        ext = get_extension(data['photo'])
        filename = str(uuid.uuid4())
        save_image(data['photo'],'livre',filename + ext)
        data['photo'] = get_path(filename + ext,'livre')

        livre = LivreModel(**data)
        livre.save_to_db()
        return  {"message": CREATED.format("Livre")}, 201
    
    @classmethod
    def get(cls):
        livres = LivreModel.find_all()
        return [livre.json() for livre in livres]

class LivreUnique(Resource):
    @classmethod
    def get(cls, livre_id):
        livre = LivreModel.find_by_id(livre_id)
        if livre : 
            return livre.json()
        return{'message': NOT_FOUND.format("Livre")},404

    @classmethod
    def delete(cls, livre_id):
        livre = LivreModel.find_by_id(livre_id)
        if livre : 
            os.remove(livre.photo)
            livre.delete_from_db()
            return {'message': DELETED.format('Livre')}, 200
        return {'message': NOT_FOUND.format("Livre")}, 404

    @classmethod
    def put(cls, livre_id):
        data = _livre_put_parser.parse_args()
        livre = LivreModel.find_by_id(livre_id)

        if livre:

            if data['photo']: 
                ext = get_extension(data['photo'])
                filename = str(uuid.uuid4())
                os.remove(livre.photo)
                save_image(data['photo'],'livre',filename + ext)
                data['photo'] = get_path(filename + ext,'livre')
            else:
                data['photo'] = livre.photo

            livre.__init__(**data)
            livre.save_to_db()
            return {'message': UPDATE.format('Article')}, 200

        return{'message': NOT_FOUND.format("Article")}, 404