from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Create Users Table
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    balance = db.Column(db.Float, default=0)
    

# Create History Table
class History(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount_sent = db.Column(db.Integer)
    transaction_type = db.Column(db.String(20))
    date_sent = db.Column(db.DateTime(timezone=True), default=func.now())

    sender = db.relationship('Users', foreign_keys=[sender_id], backref=db.backref('sent_history', lazy=True))
    receiver = db.relationship('Users', foreign_keys=[receiver_id], backref=db.backref('received_history', lazy=True))


