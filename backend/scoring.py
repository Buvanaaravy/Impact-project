def score(features, theme, expected_minutes):
    if features["silence_ratio"] > 0.6:
        return 0, "Too much silence"

    clarity = min(10, features["wpm"] / 15)
    engagement = min(10, features["pitch_variance"] / 50)
    confidence = min(10, features["face_presence"] * 10)

    theme_bonus = {"JAM": 0, "JAZZ": 5, "JIVE": 10}[theme]

    duration_penalty = 0
    if abs(features["duration"] - expected_minutes * 60) > 15:
        duration_penalty = -5

    final = clarity + engagement + confidence + theme_bonus + duration_penalty
    return round(final, 2), "OK"
