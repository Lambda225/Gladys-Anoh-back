import os
from flask_restful import Resource, reqparse
from models.podcast_model import PodcastModel
from libs.image_helper import get_extension,get_path,save_image
import uuid
import werkzeug
from models.categorie_podcast_model import CatPodcastModel
from flask_jwt_extended import jwt_required, get_jwt
from constants import * 

_podcast_parser = reqparse.RequestParser()
_podcast_parser.add_argument('titre', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("titre"))
_podcast_parser.add_argument('description', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("description"))
_podcast_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',required=True,
                                help=BLANK_ERROR.format('photo') )
_podcast_parser.add_argument('ifram', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("ifram"))
_podcast_parser.add_argument('cat_id', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("cat_id"))

_podcast_put_parser = _podcast_parser.copy()
_podcast_put_parser.remove_argument('photo')
_podcast_put_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',
                                help=BLANK_ERROR.format('photo') )

class PodcastRegister(Resource):
    @classmethod
    def post(cls):
        data = _podcast_parser.parse_args()
        cat_podcast = CatPodcastModel.find_by_id(data['cat_id'])
        if cat_podcast is None:
            {'message':NOT_FOUND.format('Catégorie Podcast')}

        if PodcastModel.find_by_name(data['titre']):
            return {'message' : NAME_ALREADY_EXIST.format('Podcast', data['titre'])}, 400
        
        ext = get_extension(data['photo'])
        filename = str(uuid.uuid4())
        save_image(data['photo'],'podcast',filename + ext)
        data['photo'] = get_path(filename + ext,'podcast')

        podcast = PodcastModel(**data)
        podcast.save_to_db()

        return {'message' : CREATED.format('Podcast')}, 200

    @classmethod
    def get(cls):
        podcasts = PodcastModel.find_all()
        if podcasts is None:
            return {'message' : NOT_FOUND.format('Podcast')}, 404
        return [podcast.json() for podcast in podcasts], 200

class PodcastUnique(Resource):
    @classmethod
    def get(cls, pod_id):
        podcast = PodcastModel.find_by_id(pod_id)
        if podcast : 
            return podcast.json()
        return{'message': NOT_FOUND.format("Podcast")}

    @classmethod
    def delete(cls, pod_id):
        podcast = PodcastModel.find_by_id(pod_id)
        if podcast : 
            os.remove(podcast.photo)
            podcast.delete_from_db()    
            return {'message': DELETED.format('Podcast')}, 200
        return {'message': NOT_FOUND.format("Podcast")}, 404

    @classmethod
    def put(cls, pod_id):
        data = _podcast_put_parser.parse_args()
        podcast = PodcastModel.find_by_id(pod_id)

        if podcast:
            if data['photo']: 
                ext = get_extension(data['photo'])
                filename = str(uuid.uuid4())
                os.remove(podcast.photo)
                save_image(data['photo'],'podcast',filename + ext)
                data['photo'] = get_path(filename + ext,'podcast')
            else:
                data['photo'] = podcast.photo

            podcast.__init__(**data)
            podcast.save_to_db()
            return {'message': UPDATE.format('Podcast')}, 200

        return{'message': NOT_FOUND.format("Podcast")},404
