from flask import Blueprint, request, jsonify
from app.models import User

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/', methods=['GET'])
def get_users():
    users = User.get_all()
    return jsonify(users)


@users_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    user.save()
    return jsonify({'message': 'User created successfully'}), 201
