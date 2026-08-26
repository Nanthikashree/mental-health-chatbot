"""
Hardcoded, non-diagnostic response templates based on mood prediction
and trend state. Deliberately rule-based (not AI-generated) for the
same reason as the safety layer: predictability and auditability matter
more than variety for a safety-sensitive prototype.

RULE: describe the pattern observed, never name a condition.
"""

def get_daily_message(mood_probs):
    """
    Given a day's mood prediction (Negative/Neutral/Positive probabilities),
    returns a short, supportive, non-diagnostic message for that single check-in.
    """
    dominant = max(mood_probs, key=mood_probs.get)

    messages = {
        "Positive": "Glad to hear things have felt good today.",
        "Neutral": "Thanks for checking in today — noted how things have been going.",
        "Negative": "Sounds like today was harder than usual. That's worth acknowledging."
    }

    return messages.get(dominant, "Thanks for checking in today.")


def get_trend_message(trend_result):
    """
    Given a trend detection result (from trend_model.detect_trend),
    returns a supportive, non-diagnostic message about the overall pattern.
    """
    trend = trend_result.get("trend")

    if trend == "Not enough data yet":
        needed = trend_result.get("checkins_needed", 21)
        so_far = trend_result.get("checkins_so_far", 0)
        remaining = needed - so_far
        return f"Keep checking in daily — trend insights will be available in about {remaining} more day(s)."

    if trend == "No check-ins yet":
        return "Start checking in daily to begin tracking how things are going over time."

    messages = {
        "Stable": "Things have felt steady for you lately — that's good to notice.",
        "Low": "The last few days have felt a bit harder than usual.",
        "Declining": (
            "It looks like the last while has felt tougher than usual. "
            "It might help to talk to someone you trust, or a mental health professional, "
            "about how you've been feeling."
        )
    }

    return messages.get(trend, "Here's how things have been trending.")