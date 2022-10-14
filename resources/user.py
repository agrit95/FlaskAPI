from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Required')
    parser.add_argument('password', type=str, required=True, help='Required')

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_name(data['username']):
            return {'message': f'User already exists'}, 400
        else:
            # or UserModel(**data) because it's a dictionary
            user = UserModel(**data)
            user.save_to_db()
            return {'message': f'User created successfully'}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()
    

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'Used deleted'}, 200
