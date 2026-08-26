from models.user_model import db
from datetime import datetime

class MoodPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_id = db.Column(db.Integer, db.ForeignKey('check_in.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    physical_wellbeing = db.Column(db.String(10), nullable=False)   # Low/Medium/High
    social_connection = db.Column(db.String(10), nullable=False)
    stress_load = db.Column(db.String(10), nullable=False)
    positive_engagement = db.Column(db.String(10), nullable=False)

    mood_negative = db.Column(db.Float, nullable=False)
    mood_neutral = db.Column(db.Float, nullable=False)
    mood_positive = db.Column(db.Float, nullable=False)