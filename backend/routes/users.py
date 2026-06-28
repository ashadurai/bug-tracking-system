from flask import Blueprint, request, jsonify
from extensions import db
from models import User

users_bp = Blueprint('users', __name__)

# GET all users
@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users], 'count': len(users)})

# GET single user
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# POST create user
@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    user = User(
        name=data['name'],
        email=data['email'],
        password=data.get('password', 'default_password'),
        role=data.get('role', 'Developer')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201

# PUT update user
@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if data.get('name'): user.name = data['name']
    if data.get('role'): user.role = data['role']
    if data.get('status'): user.status = data['status']
    db.session.commit()
    return jsonify({'message': 'User updated', 'user': user.to_dict()})

# DELETE user
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
