import random
import os
from flask import Flask, request, json, session
from flask import render_template, redirect
from twilio.rest import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  #secret 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    fName = request.form['firstName']
    pNumber = '+91' + request.form['phoneNumber']
    val = getOtpApi(pNumber)
    if val:
        return render_template('enterOTP.html')
    else:
        return 'OTP not successful'

@app.route('/validateOTP', methods=['POST'])
def validateOTP():
    otp = request.form['Otp']
    if 'response' in session:
        s = session['response']
        session.pop('response', None)
        if s == otp:
            return 'You are authorized!'
        else:
            return 'You are not authorized!'    

def generateOTP():
    return random.randrange(100000,999999)

def getOtpApi(pNumber):
    account_sid = os.getenv('ACCOUNT_SID')  #secret
    auth_token = os.getenv('AUTH_TOKEN')     #secret
    OTP = generateOTP()
    body = 'Your otp is ' + str(OTP)
    session['response'] = str(OTP)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                     body= body,
                     from_='+12202205492',
                     to=pNumber)
    
    if message.sid:
        return True
    else:
        return False

@app.route('/resendOTP', methods = ['POST', 'GET'])
def resendOTP():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)