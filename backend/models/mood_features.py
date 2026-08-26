def bucket_score(score, low_threshold, high_threshold):
    """Convert a numeric average into Low/Medium/High category."""
    if score <= low_threshold:
        return "Low"
    elif score <= high_threshold:
        return "Medium"
    else:
        return "High"


def compute_physical_wellbeing(sleep_quality, energy_level, ate_regularly, physical_activity):
    # Convert yes/no to 1-5 scale equivalent for averaging
    ate_score = 5 if ate_regularly else 1
    activity_score = 5 if physical_activity else 1
    avg = (sleep_quality + energy_level + ate_score + activity_score) / 4
    return bucket_score(avg, 2.5, 3.75)


def compute_social_connection(social_interaction, felt_connected):
    interaction_score = 5 if social_interaction else 1
    avg = (interaction_score + felt_connected) / 2
    return bucket_score(avg, 2.5, 3.75)


def compute_stress_load(stress_level, felt_overwhelmed):
    # NOTE: higher stress_level and overwhelmed = worse, so this is inverted later
    overwhelmed_score = 5 if felt_overwhelmed else 1
    avg = (stress_level + overwhelmed_score) / 2
    return bucket_score(avg, 2.5, 3.75)


def compute_positive_engagement(felt_motivated, enjoyed_something):
    enjoyed_score = 5 if enjoyed_something else 1
    avg = (felt_motivated + enjoyed_score) / 2
    return bucket_score(avg, 2.5, 3.75)


def compute_all_features(checkin):
    return {
        "physical_wellbeing": compute_physical_wellbeing(
            checkin.sleep_quality, checkin.energy_level,
            checkin.ate_regularly, checkin.physical_activity
        ),
        "social_connection": compute_social_connection(
            checkin.social_interaction, checkin.felt_connected
        ),
        "stress_load": compute_stress_load(
            checkin.stress_level, checkin.felt_overwhelmed
        ),
        "positive_engagement": compute_positive_engagement(
            checkin.felt_motivated, checkin.enjoyed_something
        ),
    }