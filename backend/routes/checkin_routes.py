from flask import Blueprint, request, jsonify, session
from models.user_model import db
from models.checkin_model import CheckIn

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
        free_text=data.get('free_text')  # optional, so use .get()
    )

    db.session.add(new_checkin)
    db.session.commit()

    return jsonify({"message": "Check-in submitted successfully", "checkin_id": new_checkin.id}), 201


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