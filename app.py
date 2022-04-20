from datetime import datetime, timedelta
import os

from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from db import db
from models import Users


app = Flask(__name__)
cors = CORS(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'bequotism@gmail.com'
app.config['MAIL_PASSWORD'] = 'optimisticc'
app.config['MAIL_USE_TLS'] = True

app.config['SECRET_KEY'] = 'fb701a23e4c6c3edfbbdeffc5142e679'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)


db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return 'Server is running!'


@app.route('/register', methods=['POST'])
def register():
    try:
        rjson = request.get_json()
        username = rjson.get('username')
        phoneno = rjson.get('phoneno')
        created_at = rjson.get('created_at')
        if username and phoneno and created_at:
            user_find = Users.query.filter_by(username=username).first()
            if not user_find:
                add_user = Users(
                    username=username,
                    phoneno=phoneno,
                    created_at=created_at
                )
                db.session.add(add_user)
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': 'User added successfully',
                    'data': {
                        'username': username,
                        'phoneno': phoneno,
                        'created_at': created_at
                    }
                }), 201
            else:
                return jsonify({
                    'status': 'failure',
                    'message': 'User already exists',
                    'data': None
                }), 409
        else:
            return jsonify({
                'status': 'failure',
                'message': 'username, phoneno and created_at are required',
                'data': None
            }), 400
    except KeyError as e:
        return jsonify({
            "status": "failure",
            "message": str(e),
            "data": None
        }), 400
    except Exception as e:
        return jsonify({
            "status": "failure",
            "message": str(e),
            "data": None
        }), 500


@app.route('/get-users', methods=['POST'])
def get_users():
    try:
        rjson = request.get_json()
        recipients = rjson.get('recipients')
        if recipients:
            test_data = []
            for i in range(1, 11):
                get_users = Users.query.filter_by(created_at=( datetime.today() - timedelta(days=i) ).strftime('%Y-%m-%d')).count()
                test_data.append({
                    'date': ( datetime.today() - timedelta(days=i) ).strftime('%Y-%m-%d'),
                    'count': get_users
                })
            msg = Message()
            msg.subject = 'Sending Users Count'
            msg.sender = app.config['MAIL_USERNAME']
            msg.body = f"""
            Users Count: {test_data}
            """
            msg.recipients = recipients
            mail.send(msg)
            return jsonify({
                'status': 'success',
                'message': 'Mail Sent Successfully!',
                'data': test_data
            }), 200
        else:
            return jsonify({
                'status': 'failure',
                'message': 'recipients are required',
                'data': None
            }), 400
    except KeyError as e:
        return jsonify({
            "status": "failure",
            "message": str(e),
            "data": None
        }), 400
    except Exception as e:
        return jsonify({
            "status": "failure",
            "message": str(e),
            "data": None
        }), 500

