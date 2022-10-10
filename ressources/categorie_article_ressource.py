import os
from asyncio import events
from flask_restful import Resource, reqparse
from constants import *
import werkzeug
from models.categorie_article_model import CatArticleModel
import uuid
from libs.image_helper import get_extension,get_path,save_image

_cat_article_parser = reqparse.RequestParser()
_cat_article_parser.add_argument('titre',type=str,location='form',required=True,help=BLANK_ERROR.format('titre'))
_cat_article_parser.add_argument('description',type=str,location='form',required=True,help=BLANK_ERROR.format('description'))
_cat_article_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage,location='files',required=True,help=BLANK_ERROR.format('photo') )

_cat_article_put_parser = _cat_article_parser.copy()
_cat_article_put_parser.remove_argument('photo')
_cat_article_put_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',
                                help=BLANK_ERROR.format('photo') )

class CatArticleList(Resource):
    @classmethod
    def post(cls):
        data = _cat_article_parser.parse_args()
        if CatArticleModel.find_by_name(data['titre']):
            return {'message' : NAME_ALREADY_EXIST.format('Cartegorie Article',data['titre'])}, 400

        ext = get_extension(data['photo'])
        filename = str(uuid.uuid4())
        save_image(data['photo'],'categorie_article',filename + ext)
        data['photo'] = get_path(filename + ext,'categorie_article')

        cat_article = CatArticleModel(**data)
        cat_article.save_to_db()

        return {'message' : CREATED.format('Categorie Article')}, 201

    @classmethod
    def get(cls):
        cat_articles = CatArticleModel.find_all()
        if not cat_articles:
            return {'message': NOT_FOUND.format('Categorie Article')}, 404
        return [cat_article.json() for cat_article in cat_articles], 200



class CatArticle(Resource):
    @classmethod
    def get(cls, cat_id):
        cat_article = CatArticleModel.find_by_id(cat_id)
        if cat_article:
            return cat_article.json()
        return {'message': NOT_FOUND.format('Categorie Article')}
    
    @classmethod
    def delete(cls, cat_id):
        cat_article = CatArticleModel.find_by_id(cat_id)
        if cat_article:
            for art in cat_article.articles:
                os.remove(art.photo)
            os.remove(cat_article.photo)
            cat_article.delete_from_db()
            return {'message':DELETED.format('Categorie Article')}, 200
        return {'message':NOT_FOUND.format('Categorie Article')}, 404

    @classmethod
    def put(cls, cat_id):
        cat_article = CatArticleModel.find_by_id(cat_id)
        data = _cat_article_put_parser.parse_args()

        if cat_article is None:
            return {'message' : NOT_FOUND.format('Categorie Article')}, 404
        else:
            if data['photo']: 
                ext = get_extension(data['photo'])
                filename = str(uuid.uuid4())
                os.remove(cat_article.photo)
                save_image(data['photo'],'categorie_article',filename + ext)
                data['photo'] = get_path(filename + ext,'categorie_article')
            else:
                data['photo'] = cat_article.photo

            cat_article.__init__(**data)
            cat_article.save_to_db()
            return {'message':UPDATE.format('Categorie Article')}
