import os
from flask_restful import Resource, reqparse
from models.event_model import EventModel
import werkzeug
import uuid
from libs.image_helper import get_extension,get_path,save_image
from constants import *



_event_parser = reqparse.RequestParser()
_event_parser.add_argument('titre', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("titre"))
_event_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',required=True,
                                help=BLANK_ERROR.format('photo') )
_event_parser.add_argument('description', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("description"))
_event_parser.add_argument('cout', type=int, required=True,location='form',
                            help=BLANK_ERROR.format("cout"))
_event_parser.add_argument('date', type=str, required=True,location='form',
                            help=BLANK_ERROR.format("date"))
_event_parser.add_argument('nom_de_place', type=int, required=True,location='form',
                            help=BLANK_ERROR.format("nom_de_place"))
_event_parser.add_argument('presentiel', type=bool, required=True,location='form',
                            help=BLANK_ERROR.format("presentiel"))

_event_put_parser = _event_parser.copy()
_event_put_parser.remove_argument('photo')
_event_put_parser.add_argument('photo',type=werkzeug.datastructures.FileStorage
                                ,location='files',
                                help=BLANK_ERROR.format('photo') )


class EventRegister(Resource):
    @classmethod
    def post(cls):
        data = _event_parser.parse_args()
        if EventModel.find_by_name(data['titre']):
            return {"message":NAME_ALREADY_EXIST.format("event", data['titre'])}, 400

        ext = get_extension(data['photo'])
        filename = str(uuid.uuid4())
        save_image(data['photo'],'event',filename + ext)
        data['photo'] = get_path(filename + ext,'event')

        event = EventModel(**data)
        event.save_to_db()
        return  {"message": CREATED.format("event")}, 201

    @classmethod
    def get(cls):
        events = EventModel.find_all()
        if events is None:
            return {'message' : NOT_FOUND.format('Sous theme')}, 404
        return [event.json() for event in events], 200

class EventUnique(Resource):
    @classmethod
    def get(cls, event_id):
        theme = EventModel.find_by_id(event_id)
        if theme : 
            return theme.json()
        return{'message': NOT_FOUND.format("Sous theme")}

    @classmethod
    def delete(cls, event_id):
        event = EventModel.find_by_id(event_id)
        if event : 
            os.remove(event.photo)
            event.delete_from_db()
            return {'message': DELETED.format('Event')}, 200
        return {'message': NOT_FOUND.format("Event")}, 404

    @classmethod
    def put(cls, event_id):
        data = _event_put_parser.parse_args()
        event = EventModel.find_by_id(event_id)

        if event:

            if data['photo']: 
                ext = get_extension(data['photo'])
                filename = str(uuid.uuid4())
                os.remove(event.photo)
                save_image(data['photo'],'event',filename + ext)
                data['photo'] = get_path(filename + ext,'event')
            else:
                data['photo'] = event.photo

            event.__init__(**data)
            event.save_to_db()
            return {'message': UPDATE.format('Event')}, 200

        return{'message': NOT_FOUND.format("Event")}, 404