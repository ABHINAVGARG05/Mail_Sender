from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
import pandas as pd
import os


app = Flask(__name__)

app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT']= int(os.getenv('MAIL_PORT',587))
app.config['MAIL_USERNAME']= os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS']= os.getenv('MAIL_USE_TLS')== 'True'
app.config['MAIL_USE_SSL']= os.getenv('MAIL_USE_SSL') == 'True'

email = Mail(app)


@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')
@app.route('/upload',methods = ['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        csv = pd.read_csv(file)
        if csv['email_id'].isnull().sum() != 0:
            return render_template('error.html')
        for index,row in csv.iterrows():
            msg = Message(
                subject = 'Hello from Abhinav Garg',
                recipients=[row['email_id']],
                sender = 'Abhinav <abhichhrp@gmail.com>'
            )
            msg.body = row.get('message')
            email.send(msg)
        return render_template("success.html")
    return "Invalid file format"
if __name__ == '__main__':
    app.run(debug = True)