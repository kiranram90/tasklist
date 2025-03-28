from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db
from models.user import User


auth_bp = Blueprint('/auth_bp',__name__)

@auth_bp.route('signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('username')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if User.query.filter(User.username == username) | (User.email == email).first():
        return jsonify({'error' : 'Username or email already exist'}), 400
        
    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.username.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200
