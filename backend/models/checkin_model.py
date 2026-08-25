from models.user_model import db
from datetime import datetime

class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sleep_quality = db.Column(db.Integer, nullable=False)       # 1-5
    energy_level = db.Column(db.Integer, nullable=False)        # 1-5
    ate_regularly = db.Column(db.Boolean, nullable=False)
    physical_activity = db.Column(db.Boolean, nullable=False)
    social_interaction = db.Column(db.Boolean, nullable=False)
    felt_connected = db.Column(db.Integer, nullable=False)      # 1-5
    stress_level = db.Column(db.Integer, nullable=False)        # 1-5
    felt_overwhelmed = db.Column(db.Boolean, nullable=False)
    overall_mood = db.Column(db.Integer, nullable=False)        # 1-5
    felt_motivated = db.Column(db.Integer, nullable=False)      # 1-5
    enjoyed_something = db.Column(db.Boolean, nullable=False)
    free_text = db.Column(db.Text, nullable=True)               # optional