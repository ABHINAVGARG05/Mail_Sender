from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User
from db.database import initialize_db, Config
from flask_mail import Mail, Message
import pandas as pd
import os
from flask_cors import cross_origin
from services.auth_services import register_user, login_user
from services.email_service import send_bulk_emails
from models.mail_data import EmailRecords
from flask_cors import CORS



app = Flask(__name__)

app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT']= int(os.getenv('MAIL_PORT',587))
app.config['MAIL_USERNAME']= os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS']= os.getenv('MAIL_USE_TLS')== 'True'
app.config['MAIL_USE_SSL']= os.getenv('MAIL_USE_SSL') == 'True'
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

email = Mail(app)

jwt = JWTManager(app)

initialize_db()
from flask_cors import CORS

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://mfc-mailman.vercel.app"}})
@cross_origin()

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = register_user(data)
    return jsonify(response),status_code

@app.route('/login',methods = ['POST'])
def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return jsonify(response),status_code


@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/upload',methods = ['POST'])
@jwt_required()
def upload():
    current_user = get_jwt_identity()

    if not current_user['isAdmin']:
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    
    file = request.files.get('file')
    return send_bulk_emails(email, file)

@app.route('/get-mails',methods = ['GET'])
@jwt_required()
def get_mail():
    current_user = get_jwt_identity()

    if not current_user['isAdmin']:
        return jsonify({"error": "Unauthorized: Admin access required"}), 403
    
    records = EmailRecords.objects()
    result = [
        {
            "recipient": record.recipient,
            "subject": record.subject,
            "message": record.message,
            "timestamp": record.timestamp,
            "sender": record.sender.username 
        }
        for record in records
    ]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug = True)