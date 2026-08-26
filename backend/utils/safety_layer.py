# Hardcoded distress indicators - deliberately simple and auditable.
# This is NOT sentiment analysis - it's direct keyword/phrase matching
# for known high-risk language patterns.

DISTRESS_KEYWORDS = [
    "kill myself", "end my life", "want to die", "not worth living",
    "better off dead", "can't go on", "no reason to live",
    "hurt myself", "self harm", "self-harm", "suicidal", "suicide",
    "ending it all", "give up on life"
]


def check_for_distress(text):
    """
    Scans free text for hardcoded distress indicators.
    Returns True if any match is found, False otherwise.
    Case-insensitive, simple substring matching - intentionally
    conservative (may over-trigger, which is the safer failure mode).
    """
    if not text:
        return False

    text_lower = text.lower()
    return any(phrase in text_lower for phrase in DISTRESS_KEYWORDS)


def get_safety_response():
    """
    Returns the fixed, non-diagnostic safety message shown when
    distress is detected. Never overridden or altered dynamically.
    """
    return {
        "triggered": True,
        "message": (
            "It sounds like you might be going through something really difficult right now. "
            "You don't have to face this alone. Please consider reaching out to someone you trust, "
            "or a mental health professional, about how you're feeling."
        ),
        "resources": [
            {"name": "iCall (India)", "contact": "9152987821", "available": "Mon-Sat, 10am-8pm"},
            {"name": "AASRA", "contact": "9820466726", "available": "24/7"},
            {"name": "Vandrevala Foundation", "contact": "1860-2662-345", "available": "24/7"}
        ]
    }