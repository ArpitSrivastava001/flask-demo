from datetime import datetime

from db import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    phoneno = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.String(80))
    def __init__(self, username, phoneno, created_at):
        self.username = username
        self.phoneno = phoneno
        self.created_at = created_at