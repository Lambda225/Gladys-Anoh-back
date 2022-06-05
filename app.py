from flask import Flask, jsonify
from flask_restful import  Api
from flask_jwt_extended import JWTManager

#user define import
from db import db
from ressources.user_resource import UserRegister, User, UserLogin, UserLogout
from ressources.token_ressource import TokenRefresh
from blocklist import BLOCKLIST



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key="rauche"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklst(jwt_header, jwt_payload):
    # jti = jwt_payload['jti']
    return (jti:=jwt_payload['jti']) in BLOCKLIST # avec operateurs walrus



api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')


if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True, port=5000)
