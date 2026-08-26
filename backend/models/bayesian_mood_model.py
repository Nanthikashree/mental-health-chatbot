from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import itertools

# Define the network structure: 4 parent nodes -> 1 child node (Mood State)
model = DiscreteBayesianNetwork([
    ('PhysicalWellbeing', 'MoodState'),
    ('SocialConnection', 'MoodState'),
    ('StressLoad', 'MoodState'),
    ('PositiveEngagement', 'MoodState'),
])

# Each parent node has 3 states: Low(0), Medium(1), High(2)
cpd_physical = TabularCPD(variable='PhysicalWellbeing', variable_card=3,
                           values=[[0.33], [0.34], [0.33]])

cpd_social = TabularCPD(variable='SocialConnection', variable_card=3,
                         values=[[0.33], [0.34], [0.33]])

cpd_stress = TabularCPD(variable='StressLoad', variable_card=3,
                         values=[[0.33], [0.34], [0.33]])

cpd_engagement = TabularCPD(variable='PositiveEngagement', variable_card=3,
                             values=[[0.33], [0.34], [0.33]])


def score_to_mood_distribution(physical, social, stress, engagement):
    """
    Convert 4 category scores (0=Low, 1=Medium, 2=High) into a probability
    distribution over MoodState: [Negative, Neutral, Positive]

    StressLoad is inverted since High stress is bad for mood.
    """
    stress_inverted = 2 - stress  # High(2) becomes Low(0) impact, Low(0) becomes High(2) impact

    total = physical + social + stress_inverted + engagement  # range: 0 to 8
    max_total = 8

    # Normalize total score to 0-1 range
    normalized = total / max_total

    # Map normalized score to a probability distribution
    # Higher normalized score = more weight on Positive, less on Negative
    positive_prob = 0.1 + (normalized * 0.8)   # ranges ~0.1 to 0.9
    negative_prob = 0.1 + ((1 - normalized) * 0.8)  # inverse
    neutral_prob = 1 - positive_prob - negative_prob

    # Safety clamp in case of rounding issues
    neutral_prob = max(neutral_prob, 0.05)

    # Re-normalize to ensure they sum to 1
    total_prob = negative_prob + neutral_prob + positive_prob
    return [negative_prob / total_prob, neutral_prob / total_prob, positive_prob / total_prob]


# Generate all 81 combinations (3^4) and build the CPT values programmatically
states = [0, 1, 2]  # Low, Medium, High
combinations = list(itertools.product(states, repeat=4))  # (physical, social, stress, engagement)

mood_values = [[], [], []]  # [Negative row, Neutral row, Positive row]

for physical, social, stress, engagement in combinations:
    dist = score_to_mood_distribution(physical, social, stress, engagement)
    mood_values[0].append(dist[0])  # Negative
    mood_values[1].append(dist[1])  # Neutral
    mood_values[2].append(dist[2])  # Positive

cpd_mood = TabularCPD(
    variable='MoodState', variable_card=3,
    values=mood_values,
    evidence=['PhysicalWellbeing', 'SocialConnection', 'StressLoad', 'PositiveEngagement'],
    evidence_card=[3, 3, 3, 3]
)

# Add all CPDs to the model
model.add_cpds(cpd_physical, cpd_social, cpd_stress, cpd_engagement, cpd_mood)

# Verify the model is valid
assert model.check_model()

# Inference engine - this is what we use to actually query the model
inference = VariableElimination(model)


def predict_mood(physical_wellbeing, social_connection, stress_load, positive_engagement):
    """
    Takes Low/Medium/High strings for each composite feature,
    returns probability distribution over Negative/Neutral/Positive mood.
    """
    category_map = {"Low": 0, "Medium": 1, "High": 2}

    result = inference.query(
        variables=['MoodState'],
        evidence={
            'PhysicalWellbeing': category_map[physical_wellbeing],
            'SocialConnection': category_map[social_connection],
            'StressLoad': category_map[stress_load],
            'PositiveEngagement': category_map[positive_engagement],
        }
    )

    return {
        "Negative": round(result.values[0], 3),
        "Neutral": round(result.values[1], 3),
        "Positive": round(result.values[2], 3),
    }