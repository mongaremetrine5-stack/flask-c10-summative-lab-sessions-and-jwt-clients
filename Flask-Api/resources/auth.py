from flask_restful import Resource
from flask import request
from models import db, User
from flask_jwt_extended import create_access_token


class Register(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password required"}, 400

        if User.query.filter_by(username=username).first():
            return {"error": "User already exists"}, 400

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401

        token = create_access_token(identity=user.id)

        return {
            "access_token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, 200