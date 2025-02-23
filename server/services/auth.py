import jwt  # Make sure this is PyJWT
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models.user import User, users

JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = 'HS256'

def generate_token(username: str) -> str:
    return jwt.encode(
        {"username": username, "exp": datetime.utcnow() + timedelta(days=1)},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        
        if not token:
            return jsonify({'message': 'Missing token'}), 401
            
        try:
            payload = verify_token(token)
            if payload['username'] not in users:
                raise Exception('User not found')
        except Exception as e:
            return jsonify({'message': str(e)}), 401
            
        return f(*args, **kwargs)
    return decorated
