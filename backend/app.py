from flask import Flask
from flask_cors import CORS
from models.user_model import db
from models.checkin_model import CheckIn
from auth import auth_bp
from routes.checkin_routes import checkin_bp
from models.mood_prediction_model import MoodPrediction

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SECRET_KEY'] = 'dev-secret-key-change-this-later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(checkin_bp, url_prefix='/api/checkin')

@app.route('/')
def home():
    return {"message": "Mood Tracker backend is running"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)