import bcrypt
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField
from datetime import datetime
from models.user import User

class EmailRecords(Document):
    recipient = StringField(required=True)
    subject = StringField(required=True)
    message = StringField(required = True)
    sender = ReferenceField(User, required=True)
    timestamp = DateTimeField(default=datetime.utcnow)