from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from database import db
from models import User
import bcrypt


auth = Blueprint("auth", __name__)
user_collection = db["users"]

@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user = User(**data)

        if user_collection.find_one({"email": user.email}):
            return {"error": "User already exists"}, 400

        hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

        user_collection.insert_one({
            "email": user.email,
            "password": hashed
        })

        return {"message": "User created"}, 201

    except Exception as e:
        return {"error": str(e)}, 400

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = user_collection.find_one({"email": email})
    if not user:
        return {"error": "User not found"}, 404

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return {"error": "Wrong password"}, 401

    token = create_access_token(identity=email)
    return {"token": token}, 200