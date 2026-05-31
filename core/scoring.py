def compute_esg_score(responses: dict[str, float | int]) -> float:
    """
    Compute a normalized ESG score (0–100) from per-indicator responses (0–5).

    The app stores responses keyed by indicator ID (e.g., E1..G3), but the scoring
    function only needs the numeric values.
    """
    if not responses:
        return 0.0

    total = float(sum(responses.values()))
    max_score = len(responses) * 5
    return round((total / max_score) * 100, 2)
