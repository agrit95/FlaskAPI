from db import db
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import User, UserRegister, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

# app.config['DEBUG'] = True


uri = os.getenv("DATABASE_URL")
# or other relevant config var
if uri.startswith("postgres://"):  # type: ignore
    uri = uri.replace("postgres://", "postgresql://", 1)  # type: ignore
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

# Only for local run
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#     'DATABASE_URL', 'sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "9jxpe7jrw8has9"
api = Api(app)

jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"isAdmin": True}
    return {"isAdmin": False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"description": "token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"description": "signature verification failed", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(errro):
    return (
        jsonify(
            {
                "description": "request does not contain an access token",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify({"description": "token is not fresh", "error": "fresh_token_required"}),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify({"description": "token has been revoked", "error": "token_revoked"}),
        401,
    )


BLOCKLIST = {2, 3}


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST


db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
