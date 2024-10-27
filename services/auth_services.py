from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from db.database import initialize_db, Config
from flask_mail import Mail, Message
import pandas as pd
import os

def register_user(data):
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.objects(username = username):
        return {"error":"User Alredy Exists"},400
    
    user = User(username = username)
    user.encrypt_password(password)
    user.save()

    return {"message": "User registered successfully"}, 201

def login_user(data):
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.objects(username = username).first()
    if user and user.check_password(password):
        token = create_access_token(identity = {
            "id": str(user.id),
            "username": user.username,
            "isAdmin": user.isAdmin
        })
        return {"token":token},200
    return {"error":"Invalid Credentials"},400