import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Required')
    parser.add_argument('password', type=str, required=True, help='Required')

    def post(self):
        data = self.parser.parse_args()
        username = data['username'].strip().lower()
        password = data['password'].strip().lower()

        if UserModel.find_username(username):
            return {'message': f'User {username} already exists'}, 400
        else:
            # or UserModel(**data) because it's a dictionary
            user = UserModel(username=username, password=password)
            user.save_to_db()
            return {'message': f'User {username} created successfully'}, 201
