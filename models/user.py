import bcrypt
from mongoengine import Document, StringField, BooleanField

class User(Document):
    username = StringField(required = True,unique = True)
    password = StringField(required = True,unique = True)
    isAdmin = BooleanField(default = False)

    def encrypt_password(self,password):
        #hashing the password
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        #check the hashed password
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))