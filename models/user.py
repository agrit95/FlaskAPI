from db import db


class UserModel(db.Model):
    # showing sqlalchemy the tables name where these models are going to be stored
    __tablename__ = 'users'
    # also the columns the table users contains
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
