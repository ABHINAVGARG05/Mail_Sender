import os
from mongoengine import connect

class Config():
    MONGODB_URI = os.getenv('MONGODB_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def initialize_db():
    connect(host = Config.MONGODB_URI)
    print("DB connected Successfully",Config.MONGODB_URI)