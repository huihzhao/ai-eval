from flask import Blueprint, request, jsonify
from models.user import User, users
from services.auth import generate_token

blueprint = Blueprint('auth', __name__)

@blueprint.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
        
    if username in users:
        return jsonify({'message': 'Username already exists'}), 400
        
    user = User(
        username=username,
        password_hash=User.hash_password(password)
    )
    users[username] = user
    
    return jsonify({'message': 'User created successfully'}), 201

@blueprint.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
        
    user = users.get(username)
    if not user or not user.verify_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = generate_token(username)
    return jsonify({'token': token}), 200
