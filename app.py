from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# from datetime import timedelta

# when working with flask_restful we no longer required jsonify
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '9jxpe7jrw8has9'
api = Api(app)


# to change the authentication url endpoint we can use below
# app.config['JWT_AUTH_URL_RULE'] = '/login'
# config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)
# jwt create a new endpoint i.e. /auth
# when we call /auth we send it username & password jwt get
# the username & password and sends it to the authenticate func
# which will autheticate the user via username & password sent.
# if match it returns the user and that becomes the identity
# next auth endpoint returns a JWT (JSON WEB TOKEN) & we can
# send it to the next request we make.


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
