# backend/models/message.py

from datetime import datetime
from ..db import db

class Message(db.Model):
    __tablename__ = 'messages'  # Ensure the table name is specified

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'assistant'
