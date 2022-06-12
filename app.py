import os
from dotenv import load_dotenv; load_dotenv(".env", verbose=True);
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
from libs.image_helper import IMAGE_SET
from blocklist import BLOCKLIST

app = Flask(__name__)
app.config.from_object("config_dev")
app.config.from_envvar('APPLICATION_SETTINGS',silent=True)

patch_request_class(app, 10 * 1024 * 1024) #10MB max size upload
configure_uploads(app, IMAGE_SET)

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
migrate=Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklst(jwt_header, jwt_payload):
    # jti = jwt_payload['jti']
    return (jti:=jwt_payload['jti']) in BLOCKLIST # avec operateurs walrus


#### resources ####
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ImageUpload, '/upload/image')
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
#### resources end ####

if __name__=='__main__':
    app.run(port=5000)
