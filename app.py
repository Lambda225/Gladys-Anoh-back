import os
from dotenv import load_dotenv

from models.event_model import EventModel; load_dotenv(".env", verbose=True);
from flask import Flask
from flask_restful import  Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate

#user define import
from db import db
from ressources.user_resource import UserRegister, User, UserLogin, UserLogout
from ressources.token_ressource import TokenRefresh
from ressources.image_resource import ImageUpload, Image, AvatarUpload, Avatar
from ressources.role_ressource import Role, RoleList
from ressources.event_ressource import EventRegister
from ressources.article_ressource import ArticleRegister
from libs.image_helper import IMAGE_SET
from blocklist import BLOCKLIST
from models.roles_model import RoleModel
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config.from_object("config_dev")
app.config.from_envvar('APPLICATION_SETTINGS',silent=True)
cors = CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

patch_request_class(app, 10 * 1024 * 1024) #10MB max size upload
configure_uploads(app, IMAGE_SET)

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
migrate=Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()
    admin = RoleModel("admin")
    admin.save_to_db()
    user = RoleModel("user")
    user.save_to_db()
    
    

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklst(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return (jti['jti']) in BLOCKLIST #jti:=jwt_payload['jti'] avec operateurs walrus


#### resources ####
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ImageUpload, '/upload/image')
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(Role, '/role/<string:name>')
api.add_resource(RoleList, '/roles')
api.add_resource(EventRegister, '/event/create')
api.add_resource(ArticleRegister, '/article/create')
#### resources end ####

if __name__=='__main__':
    app.run(port=5000)
