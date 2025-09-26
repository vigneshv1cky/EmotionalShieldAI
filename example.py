# Trader Risk Alert Matrix (Sleep × Exercise)

# Define the matrix as a dictionary of dictionaries
risk_matrix = {
    "Poor Sleep": {
        "Poor Exercise": (
            "🔴 High Risk",
            "Judgment impaired, stress high, discipline weak — avoid trading.",
        ),
        "Moderate Exercise": (
            "🔴 High Risk",
            "Some physical balance, but fatigue dominates — high chance of costly mistakes.",
        ),
        "Good Exercise": (
            "🟠 Elevated Risk",
            "Good fitness helps, but poor rest still limits focus.",
        ),
    },
    "Moderate Sleep": {
        "Poor Exercise": (
            "🔴 Elevated Risk",
            "Partial rest + inactivity = sluggish, reactive trading.",
        ),
        "Moderate Exercise": (
            "🟠 Moderate Risk",
            "Fair balance, but not peak performance — trade smaller size.",
        ),
        "Good Exercise": (
            "🟡 Caution",
            "Reasonable discipline, but not optimal endurance.",
        ),
    },
    "Good Sleep": {
        "Poor Exercise": (
            "🟠 Moderate Risk",
            "Rested mind, but low fitness = shorter stamina in volatile sessions.",
        ),
        "Moderate Exercise": (
            "🟡 Caution",
            "Balanced state, can trade cautiously with discipline.",
        ),
        "Good Exercise": (
            "🟢 Optimal",
            "Peak focus, strong discipline, reduced stress — ideal trading state.",
        ),
    },
}


def get_trader_risk_alert(sleep_level, exercise_level):
    """
    Returns the trader risk alert (symbol + text)
    based on sleep and exercise inputs.
    """
    try:
        alert, description = risk_matrix[sleep_level][exercise_level]
        return f"{alert} | {description}"
    except KeyError:
        return (
            "❓ Invalid input. Please use: Sleep = [Poor Sleep, Moderate Sleep, Good Sleep], "
            "Exercise = [Poor Exercise, Moderate Exercise, Good Exercise]."
        )
