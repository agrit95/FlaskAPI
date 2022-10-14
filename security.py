from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_name(username)
    if user and user.password == password:
        return user


def identity(payload):
    # payload is the content of JWT token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
