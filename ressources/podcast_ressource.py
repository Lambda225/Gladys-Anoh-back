from flask_restful import Resource, reqparse
from models.article_model import ArticleModel 
from flask_jwt_extended import jwt_required, get_jwt
from constants import * 

_event_parser = reqparse.RequestParser()
_event_parser.add_argument('titre', type=str, required=True,
                            help=BLANK_ERROR.format("titre"))
_event_parser.add_argument('description', type=str, required=True,
                            help=BLANK_ERROR.format("description"))

