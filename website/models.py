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

# Create History Table
class History(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    sender_email = db.Column(db.String(150))
    sender_username = db.Column(db.String(150))
    receiver_id = db.Column(db.Integer)
    receiver_email = db.Column(db.String(150))
    receiver_username = db.Column(db.String(150))
    amount_sent = db.Column(db.Integer)
    is_received = db.Column(db.Boolean)
    date_sent = db.Column(db.DateTime(timezone=True), default=func.now())
    date_received = db.Column(db.DateTime(timezone=True), default=func.now())


