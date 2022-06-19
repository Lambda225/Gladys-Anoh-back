from flask_restful import Resource, reqparse
from models.article_model import ArticleModel 
from flask_jwt_extended import jwt_required, get_jwt
from constants import * 

_event_parser = reqparse.RequestParser()
_event_parser.add_argument('titre', type=str, required=True,
                            help=BLANK_ERROR.format("titre"))
_event_parser.add_argument('description', type=str, required=True,
                            help=BLANK_ERROR.format("description"))


class ArticleRegister(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        data = _event_parser.parse_args() 
        jti = get_jwt()['jti'] #identifiant unique jwt
        print(jti)
        if ArticleModel.find_by_name(data['titre']):
            return {"message":NAME_ALREADY_EXIST.format("event", data['titre'])}, 400
        article = ArticleModel(**data)
        article.save_to_db()
        return  {"message": CREATED.format("article")}, 201
    
    @classmethod
    def get(cls):
        articles = ArticleModel.find_all()
        if not articles:
            return {'message': NOT_FOUND.format("Articles")}, 404
        return [article.json() for article in articles]