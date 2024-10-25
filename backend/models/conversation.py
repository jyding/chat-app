from datetime import datetime
from ..db import db

class Conversation(db.Model):
    __tablename__ = 'conversations'  
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship('Message', backref='conversation', lazy=True)
