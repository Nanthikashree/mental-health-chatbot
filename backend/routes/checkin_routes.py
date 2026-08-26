from flask import Blueprint, request, jsonify, session
from models.user_model import db
from models.checkin_model import CheckIn
from models.mood_prediction_model import MoodPrediction
from models.mood_features import compute_all_features
from models.bayesian_mood_model import predict_mood
from utils.safety_layer import check_for_distress, get_safety_response
from models.trend_model import detect_trend, mood_prediction_to_score
from utils.response_bank import get_daily_message, get_trend_message

checkin_bp = Blueprint('checkin', __name__)

@checkin_bp.route('/submit', methods=['POST'])
def submit_checkin():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()

    required_fields = [
        'sleep_quality', 'energy_level', 'ate_regularly', 'physical_activity',
        'social_interaction', 'felt_connected', 'stress_level', 'felt_overwhelmed',
        'overall_mood', 'felt_motivated', 'enjoyed_something'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    free_text = data.get('free_text')

    new_checkin = CheckIn(
        user_id=session['user_id'],
        sleep_quality=data['sleep_quality'],
        energy_level=data['energy_level'],
        ate_regularly=data['ate_regularly'],
        physical_activity=data['physical_activity'],
        social_interaction=data['social_interaction'],
        felt_connected=data['felt_connected'],
        stress_level=data['stress_level'],
        felt_overwhelmed=data['felt_overwhelmed'],
        overall_mood=data['overall_mood'],
        felt_motivated=data['felt_motivated'],
        enjoyed_something=data['enjoyed_something'],
        free_text=free_text
    )

    db.session.add(new_checkin)
    db.session.commit()

    if check_for_distress(free_text):
        safety_response = get_safety_response()
        return jsonify({
            "message": "Check-in submitted successfully",
            "checkin_id": new_checkin.id,
            "safety_alert": safety_response
        }), 201

    features = compute_all_features(new_checkin)

    mood_probs = predict_mood(
        features['physical_wellbeing'],
        features['social_connection'],
        features['stress_load'],
        features['positive_engagement']
    )

    new_prediction = MoodPrediction(
        checkin_id=new_checkin.id,
        user_id=session['user_id'],
        physical_wellbeing=features['physical_wellbeing'],
        social_connection=features['social_connection'],
        stress_load=features['stress_load'],
        positive_engagement=features['positive_engagement'],
        mood_negative=mood_probs['Negative'],
        mood_neutral=mood_probs['Neutral'],
        mood_positive=mood_probs['Positive']
    )

    db.session.add(new_prediction)
    db.session.commit()

    daily_message = get_daily_message(mood_probs)

    return jsonify({
        "message": "Check-in submitted successfully",
        "checkin_id": new_checkin.id,
        "mood_prediction": mood_probs,
        "daily_message": daily_message
    }), 201


@checkin_bp.route('/history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    checkins = CheckIn.query.filter_by(user_id=session['user_id']).order_by(CheckIn.timestamp.desc()).all()

    result = [{
        "id": c.id,
        "timestamp": c.timestamp.isoformat(),
        "sleep_quality": c.sleep_quality,
        "energy_level": c.energy_level,
        "overall_mood": c.overall_mood,
        "stress_level": c.stress_level,
        "free_text": c.free_text
    } for c in checkins]

    return jsonify(result), 200


@checkin_bp.route('/trend', methods=['GET'])
def get_trend():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    predictions = MoodPrediction.query.filter_by(
        user_id=session['user_id']
    ).order_by(MoodPrediction.timestamp.asc()).all()

    if not predictions:
        return jsonify({
            "trend": "No check-ins yet",
            "checkins_so_far": 0,
            "trend_message": get_trend_message({"trend": "No check-ins yet"})
        }), 200

    mood_scores = [
        mood_prediction_to_score(p.mood_negative, p.mood_neutral, p.mood_positive)
        for p in predictions
    ]

    result = detect_trend(mood_scores)
    result["trend_message"] = get_trend_message(result)

    return jsonify(result), 200