def compute_esg_score(responses):
    total = sum(responses.values())
    max_score = len(responses) * 5
    return round((total / max_score) * 100, 2)