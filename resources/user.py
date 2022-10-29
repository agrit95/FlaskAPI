from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource, reqparse
from models.user import UserModel, TokenBlocklist
from datetime import datetime, timezone


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help="Required")
_user_parser.add_argument("password", type=str, required=True, help="Required")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_name(data["username"]):
            return {"message": f"User already exists"}, 400
        else:
            # or UserModel(**data) because it's a dictionary
            user = UserModel(**data)
            user.save_to_db()
            return {"message": f"User created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "Used deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user and user.password == data["password"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": "Invalid Credentials"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        token = TokenBlocklist(jti, now)
        token.save_to_db()
        return {"message": "User Successfully Logged Out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": access_token}, 200
