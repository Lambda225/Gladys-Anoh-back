from urllib import response
from flask_restful import Resource,reqparse
from models.question_model import QuestionModel
from constants import *

_question_parser = reqparse.RequestParser()
_question_parser.add_argument('contenu', type=str,location='form',required=True,help=BLANK_ERROR.format("contenu"))

class QuestionRegister(Resource):
    @classmethod
    def post(cls):
        data = _question_parser.parse_args()

        if QuestionModel.find_by_name(data['contenu']):
            return {'message' : NAME_ALREADY_EXIST.format('Question', data['contenu'])}, 400
        
        question = QuestionModel(**data)
        question.save_to_db()
        return {'message' : CREATED.format('Question')}, 200

    @classmethod
    def get(cls):
        questions = QuestionModel.find_all()
        if questions is None:
            return {'message' : NOT_FOUND.format('Question')}, 404
        return [question.json() for question in questions], 200


class QuestionUnique(Resource):
    @classmethod
    def get(cls, quest_id):
        question = QuestionModel.find_by_id(quest_id)
        if question : 
            return question.json()
        return{'message': NOT_FOUND.format("Question")},404
    
    @classmethod
    def delete(cls, quest_id):
        question = QuestionModel.find_by_id(quest_id)
        if question : 
            question.delete_from_db()
            return {'message': DELETED.format('Question')}, 200
        return {'message': NOT_FOUND.format("Question")}, 404

    @classmethod
    def put(cls, quest_id):
        data = _question_parser.parse_args()
        question = QuestionModel.find_by_id(quest_id)

        if question:
            question.__init__(**data)
            question.save_to_db()
            return {'message': UPDATE.format('Question')}, 200

        return{'message': NOT_FOUND.format("Question")},404