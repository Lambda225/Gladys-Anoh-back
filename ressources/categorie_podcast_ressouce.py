import os
import werkzeug
import uuid
from flask_restful import Resource, reqparse
from constants import *
from libs.image_helper import get_extension,get_path,save_image
from models.categorie_podcast_model import CatPodcastModel

_cat_podcast_parser = reqparse.RequestParser()
_cat_podcast_parser.add_argument('titre',type=str,location='form',required=True,help=BLANK_ERROR.format('titre'))
_cat_podcast_parser.add_argument('description',type=str,location='form',required=True,help=BLANK_ERROR.format('description'))
_cat_podcast_parser.add_argument('lienspotify',type=str,location='form',required=True,help=BLANK_ERROR.format('lienspotify'))
_cat_podcast_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage,location='files',required=True,help=BLANK_ERROR.format('photo') )

_cat_podcast_put_parser = _cat_podcast_parser.copy()
_cat_podcast_put_parser.remove_argument('photo')
_cat_podcast_put_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',
                                help=BLANK_ERROR.format('photo') )

class CatPodcastRegister(Resource):
    @classmethod
    def post(cls):
        data = _cat_podcast_parser.parse_args()
        if CatPodcastModel.find_by_name(data['titre']):
            return {'message' : NAME_ALREADY_EXIST.format('Cartegorie Podcast',data['titre'])}, 400

        ext = get_extension(data['photo'])
        filename = str(uuid.uuid4())
        save_image(data['photo'],'categorie_podcast',filename + ext)
        data['photo'] = get_path(filename + ext,'categorie_podcast')

        cat_podcast = CatPodcastModel(**data)
        cat_podcast.save_to_db()

        return {'message' : CREATED.format('Categorie Podcast')}, 201

    @classmethod
    def get(cls):
        cat_podcasts = CatPodcastModel.find_all()
        if not cat_podcasts:
            return {'message': NOT_FOUND.format('Categorie Podcast')}, 404
        return [cat_podcast.json() for cat_podcast in cat_podcasts], 200



class CatPodcastUnique(Resource):
    @classmethod
    def get(cls, cat_id):
        cat_podcast = CatPodcastModel.find_by_id(cat_id)
        if cat_podcast:
            return cat_podcast.json()
        return {'message': NOT_FOUND.format('Categorie Podcast')}, 404
    
    @classmethod
    def delete(cls, cat_id):
        cat_podcast = CatPodcastModel.find_by_id(cat_id)
        if cat_podcast:

            for pod in cat_podcast.podcasts:
                os.remove(pod.photo)
            
            os.remove(cat_podcast.photo)
            cat_podcast.delete_from_db()
            return {'message':DELETED.format('Categorie Podcast')}, 200
        return {'message':NOT_FOUND.format('Categorie Podcast')}, 404

    @classmethod
    def put(cls, cat_id):
        cat_podcast = CatPodcastModel.find_by_id(cat_id)
        data = _cat_podcast_put_parser.parse_args()

        if cat_podcast is None:
            return {'message' : NOT_FOUND.format('Categorie Podcast')}, 404
        else:
            if data['photo']: 
                ext = get_extension(data['photo'])
                filename = str(uuid.uuid4())
                os.remove(cat_podcast.photo)
                save_image(data['photo'],'categorie_podcast',filename + ext)
                data['photo'] = get_path(filename + ext,'categorie_podcast')
            else:
                data['photo'] = cat_podcast.photo

            cat_podcast.__init__(**data)
            cat_podcast.save_to_db()
            return {'message':UPDATE.format('Categorie Podcast')}, 200
