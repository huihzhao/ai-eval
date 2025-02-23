from quart import Blueprint, request, jsonify
from models.user import User, users
from services.auth import generate_token
import traceback

blueprint = Blueprint('auth', __name__)

@blueprint.route('/register', methods=['POST'])
async def register():
    try:
        data = await request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing username or password"}), 400
            
        username = data['username']
        password = data['password']
        
        if username in users:
            return jsonify({"error": "Username already exists"}), 409
            
        users[username] = User(username=username, password=password)
        return jsonify({"message": "User registered successfully"}), 201
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Registration failed", "details": str(e)}), 500

@blueprint.route('/login', methods=['POST'])
async def login():
    try:
        data = await request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing username or password"}), 400
            
        username = data['username']
        password = data['password']
        
        if username not in users or users[username].password != password:
            return jsonify({"error": "Invalid credentials"}), 401
            
        token = generate_token(username)
        return jsonify({"token": token}), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Login failed", "details": str(e)}), 500
