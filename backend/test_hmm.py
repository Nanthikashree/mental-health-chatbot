from models.trend_model import detect_trend, mood_prediction_to_score
from models.mood_prediction_model import MoodPrediction
import numpy as np
# Case 1: Too few data points - should refuse to guess
print("=== Testing INSUFFICIENT DATA scenario ===")
few_scores = [0.5, 0.4, 0.3]
result = detect_trend(few_scores)
print(result)

# Case 2: Declining trend with 21 data points
print("\n=== Testing DECLINING scenario (21 points) ===")
declining_scores = list(np.linspace(0.6, -0.7, 21))  # smoothly worsening over 21 days
result = detect_trend(declining_scores)
print("Mood scores:", [round(s, 2) for s in declining_scores])
print("Detected trend:", result["trend"])
print("Full state sequence:", result["state_sequence"])
print("Recent window used:", result["recent_window_used"])

# Case 3: Stable trend with 21 data points
print("\n=== Testing STABLE scenario (21 points) ===")
stable_scores = [0.5, 0.45, 0.48, 0.52, 0.47, 0.5, 0.49, 0.46, 0.51, 0.48,
                  0.5, 0.47, 0.49, 0.52, 0.46, 0.5, 0.48, 0.51, 0.47, 0.5, 0.49]
result = detect_trend(stable_scores)
print("Detected trend:", result["trend"])
print("Full state sequence:", result.get("state_sequence"))
print("Recent window used:", result.get("recent_window_used", "N/A - low variance shortcut used"))