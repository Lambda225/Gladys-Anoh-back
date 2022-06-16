from flask_restful import Resource, reqparse
from models.event_model import EventModel
from constants import *



_event_parser = reqparse.RequestParser()
_event_parser.add_argument('titre', type=str, required=True,
                            help=BLANK_ERROR.format("titre"))
_event_parser.add_argument('description', type=str, required=True,
                            help=BLANK_ERROR.format("description"))
_event_parser.add_argument('cout', type=str, required=True,
                            help=BLANK_ERROR.format("cout"))
_event_parser.add_argument('date', type=str, required=True,
                            help=BLANK_ERROR.format("date"))
_event_parser.add_argument('nom_de_place', type=int, required=True,
                            help=BLANK_ERROR.format("nom_de_place"))
_event_parser.add_argument('presentiel', type=bool, required=True,
                            help=BLANK_ERROR.format("presentiel"))


class EventRegister(Resource):
    @classmethod
    def post(cls):
        data = _event_parser.parse_args()
        if EventModel.find_by_name(data['titre']):
            return {"message":NAME_ALREADY_EXIST.format("event", data['titre'])}, 400
        event = EventModel(**data)
        event.save_to_db()
        return  {"message": CREATED.format("event")}, 201