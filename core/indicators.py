"""
Canonical ESG indicator definitions used across the Streamlit app.

Important: the ML training dataset in `data/sample_training.csv` uses short indicator IDs
(E1..E3, S1..S3, G1..G3). To avoid feature-name mismatches between the self-assessment
UI and the ML predictor, we store assessment responses keyed by these IDs.
"""

ESG_INDICATORS = {
    "E": [
        {"id": "E1", "label": "Energy consumption monitoring"},
        {"id": "E2", "label": "Carbon emissions tracking"},
        {"id": "E3", "label": "Waste management policy"},
    ],
    "S": [
        {"id": "S1", "label": "Employee safety policy"},
        {"id": "S2", "label": "Diversity & inclusion"},
        {"id": "S3", "label": "Community engagement"},
    ],
    "G": [
        {"id": "G1", "label": "Board structure"},
        {"id": "G2", "label": "Anti-corruption policy"},
        {"id": "G3", "label": "Data protection"},
    ],
}


def indicator_label_by_id() -> dict[str, str]:
    """Convenience mapping for turning IDs (e.g. 'E1') into human labels."""
    mapping: dict[str, str] = {}
    for indicators in ESG_INDICATORS.values():
        for indicator in indicators:
            mapping[indicator["id"]] = indicator["label"]
    return mapping
