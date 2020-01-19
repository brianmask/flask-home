import uuid
import datetime

from app.main import db
from app.main.model.user import User

def get_a_user(public_id):
    """ Get specific user by UUID """
    return User.query.filter_by(public_id=public_id).first()

def get_all_users():
    """ Return all Users in the database """
    return User.query.all()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def save_changes(data):
    """ Save data into the database """
    db.session.add(data)
    db.session.commit()

def save_new_user(data):
    """ Save's a new user into the system """
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)

    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409