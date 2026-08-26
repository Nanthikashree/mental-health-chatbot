import numpy as np
from hmmlearn import hmm
from collections import Counter

STATE_LABELS = ["Declining", "Low", "Stable"]

MIN_CHECKINS_FOR_TREND = 21
SMOOTHING_WINDOW = 3
LOW_VARIANCE_THRESHOLD = 0.15  # if scores barely move, skip the HMM and call it Stable directly


def mood_prediction_to_score(mood_negative, mood_neutral, mood_positive):
    """
    Converts a Negative/Neutral/Positive probability distribution
    into a single numeric mood score from -1 (very negative) to +1 (very positive).
    """
    return (mood_positive * 1) + (mood_neutral * 0) + (mood_negative * -1)


def detect_trend(mood_scores):
    """
    Takes a list of daily mood scores (oldest to newest) and returns
    the detected trend label.

    Requires at least MIN_CHECKINS_FOR_TREND data points to run at all.

    Before running the HMM, checks if the data has enough variance to
    even warrant state detection - if scores are consistently tight
    (low variance), we classify directly as Stable rather than letting
    the HMM invent noise-driven state differences.
    """
    if len(mood_scores) < MIN_CHECKINS_FOR_TREND:
        return {
            "trend": "Not enough data yet",
            "checkins_so_far": len(mood_scores),
            "checkins_needed": MIN_CHECKINS_FOR_TREND,
            "state_sequence": None
        }

    recent_scores = mood_scores[-MIN_CHECKINS_FOR_TREND:]
    std_dev = np.std(recent_scores)

    # LOW VARIANCE SHORT-CIRCUIT: if mood barely moves, it's stable by definition -
    # no need to risk the HMM inventing false state changes from noise
    if std_dev < LOW_VARIANCE_THRESHOLD:
        return {
            "trend": "Stable",
            "reason": "Low variance in recent mood scores",
            "std_dev": round(float(std_dev), 3),
            "state_sequence": None,
            "mood_scores": mood_scores
        }

    X = np.array(mood_scores).reshape(-1, 1)

    model = hmm.GaussianHMM(n_components=3, covariance_type="diag", n_iter=100, random_state=42)
    model.fit(X)

    hidden_states = model.predict(X)

    state_means = model.means_.flatten()
    ranked_states = np.argsort(state_means)

    state_to_label = {
        ranked_states[0]: "Declining",
        ranked_states[1]: "Low",
        ranked_states[2]: "Stable"
    }

    full_sequence = [state_to_label[s] for s in hidden_states]

    recent_window = full_sequence[-SMOOTHING_WINDOW:]
    smoothed_trend = Counter(recent_window).most_common(1)[0][0]

    return {
        "trend": smoothed_trend,
        "std_dev": round(float(std_dev), 3),
        "state_sequence": full_sequence,
        "recent_window_used": recent_window,
        "mood_scores": mood_scores
    }