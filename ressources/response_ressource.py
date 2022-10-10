from flask_restful import Resource,reqparse
from models.question_model import QuestionModel
from models.reponse_model import ReponseModel
from constants import *

_reponse_parser = reqparse.RequestParser()
_reponse_parser.add_argument('contenu', type=str,location='form', required=True,help=BLANK_ERROR.format("contenu"))
_reponse_parser.add_argument('quest_id', type=str,location='form', required=True,help=BLANK_ERROR.format("contenu"))

class ReponseRegister(Resource):
    @classmethod
    def post(cls):
        data = _reponse_parser.parse_args()

        if ReponseModel.find_by_name(data['contenu']):
            return {'message' : NAME_ALREADY_EXIST.format('Question', data['contenu'])}, 400
        
        reponse = ReponseModel(data['contenu'])
        question = QuestionModel.find_by_id(data['quest_id'])
        reponse.questions.append(question)
        reponse.save_to_db()
        return {'message' : CREATED.format('Reponse')}, 200

    @classmethod
    def get(cls):
        reponses = ReponseModel.find_all()
        if reponses is None:
            return {'message' : NOT_FOUND.format('Reponse')}, 404
        return [reponse.json() for reponse in reponses], 200


class ReponseUnique(Resource):
    @classmethod
    def get(cls, rep_id):
        reponse = ReponseModel.find_by_id(rep_id)
        if reponse : 
            return reponse.json()
        return{'message': NOT_FOUND.format("Reponse")},404
    
    @classmethod
    def delete(cls, rep_id):
        question = ReponseModel.find_by_id(rep_id)
        if question : 
            question.delete_from_db()
            return {'message': DELETED.format('Reponse')}, 200
        return {'message': NOT_FOUND.format("Reponse")}, 404

    @classmethod
    def put(cls, rep_id):
        data = _reponse_parser.parse_args()
        reponse = ReponseModel.find_by_id(rep_id)

        if reponse:
            reponse.__init__(**data)
            reponse.save_to_db()
            return {'message': UPDATE.format('Reponse')}, 200

        return{'message': NOT_FOUND.format("Reponse")},404