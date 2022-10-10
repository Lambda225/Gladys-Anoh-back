from asyncio import events
from flask_restful import Resource, reqparse
from constants import *
from models.question_model import QuestionModel

_lier_parser = reqparse.RequestParser()
_lier_parser.add_argument('question1_id', type=str,location='form',required=True,help=BLANK_ERROR.format("question_id"))
_lier_parser.add_argument('question2_id', type=str,location='form',required=True,help=BLANK_ERROR.format("question2_id"))

class Lier(Resource):
    @classmethod
    def post(cls):
        data = _lier_parser.parse_args()

        if not QuestionModel.find_by_id(data['question1_id']):
            return {'message' : NOT_FOUND.format('Question 1')}, 404

        if not QuestionModel.find_by_id(data['question2_id']):
            return {'message' : NOT_FOUND.format('Question 2')}, 404

        question1 = QuestionModel.find_by_id(data['question1_id']) 
        question2 = QuestionModel.find_by_id(data['question2_id'])
        question2.reponse_id = question1.reponse_id

        question2.save_to_db()

        return {'message' : 'Lier avec succès'}, 200
        