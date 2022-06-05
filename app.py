from flask import Flask, jsonify
from flask_restful import  Api
from flask_jwt_extended import JWTManager

#user define import
from ressources.user_resource import UserRegister, User, UserLogin, UserLogout
from ressources.token_ressource import TokenRefresh
from ressources.item_resource import Item, ItemList
from ressources.store_resource import Store, StoreList
from blocklist import BLOCKLIST



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key="jose"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklst(jwt_header, jwt_payload):
    # jti = jwt_payload['jti']
    return (jti:=jwt_payload['jti']) in BLOCKLIST # avec operateurs walrus


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')


if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
