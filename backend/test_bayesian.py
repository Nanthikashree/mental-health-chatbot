from models.bayesian_mood_model import predict_mood

# Test case: everything good
print("All High:", predict_mood("High", "High", "Low", "High"))

# Test case: everything bad
print("All Low/High Stress:", predict_mood("Low", "Low", "High", "Low"))

# Test case: mixed
print("Mixed:", predict_mood("Medium", "Low", "High", "Medium"))