import os
from flask_restful import Resource, reqparse
from models.article_model import ArticleModel 
from models.categorie_article_model import CatArticleModel
import werkzeug
import uuid
from flask_jwt_extended import jwt_required, get_jwt
from constants import * 
from libs.image_helper import get_extension,get_path,save_image

_article_parser = reqparse.RequestParser()
_article_parser.add_argument('titre', type=str,location='form', required=True,
                            help=BLANK_ERROR.format("titre"))
_article_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',required=True,
                                help=BLANK_ERROR.format('photo_principale') )
_article_parser.add_argument('description', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("description"))
_article_parser.add_argument('cat_id', type=int, required=True,location='form',
                            help=BLANK_ERROR.format("cat_id"))

_article_put_parser = _article_parser.copy()
_article_put_parser.remove_argument('photo')
_article_put_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',
                                help=BLANK_ERROR.format('photo') )

class ArticleRegister(Resource):
    @classmethod
    # @jwt_required()
    def post(cls):
        data = _article_parser.parse_args() 
        cat_article = CatArticleModel.find_by_id(data['cat_id'])
        if cat_article is None:
            {'message': NOT_FOUND.format('Catégorie Article')}, 404

        if ArticleModel.find_by_name(data['titre']):
            return {'message' : NAME_ALREADY_EXIST.format('Article', data['titre'])}, 400
        # jti = get_jwt()['jti'] #identifiant unique jwt
        # print(jti)

        ext = get_extension(data['photo'])
        filename = str(uuid.uuid4())
        save_image(data['photo'],'article',filename + ext)
        data['photo'] = get_path(filename + ext,'article')

        article = ArticleModel(**data)
        article.save_to_db()
        return  {"message": CREATED.format("Article")}, 201
    
    @classmethod
    def get(cls):
        articles = ArticleModel.find_all()
        return [article.json() for article in articles]

class Article(Resource):
    @classmethod
    def get(cls, art_id):
        article = ArticleModel.find_by_id(art_id)
        if article : 
            return article.json()
        return{'message': NOT_FOUND.format("Article")},404

    @classmethod
    def delete(cls, art_id):
        article = ArticleModel.find_by_id(art_id)
        if article : 
            os.remove(article.photo)
            article.delete_from_db()
            return {'message': DELETED.format('Article')}, 200
        return {'message': NOT_FOUND.format("Article")}, 404

    @classmethod
    def put(cls, art_id):
        data = _article_put_parser.parse_args()
        article = ArticleModel.find_by_id(art_id)

        if article:

            if data['photo']: 
                ext = get_extension(data['photo'])
                filename = str(uuid.uuid4())
                os.remove(article.photo)
                save_image(data['photo'],'article',filename + ext)
                data['photo'] = get_path(filename + ext,'article')
            else:
                data['photo'] = article.photo

            article.__init__(**data)
            article.save_to_db()
            return {'message': UPDATE.format('Article')}, 200

        return{'message': NOT_FOUND.format("Article")}, 404