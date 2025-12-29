import warnings
from sklearn.ensemble import RandomForestRegressor

try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except Exception as e:
    XGBOOST_AVAILABLE = False
    warnings.warn(
        "XGBoost not available. Falling back to RandomForest.\n"
        f"Reason: {e}"
    )


def train_model(X, y):
    """
    Train ESG prediction model.
    Uses XGBoost if available, otherwise RandomForest.
    """

    if XGBOOST_AVAILABLE:
        model = XGBRegressor(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            objective="reg:squarederror",
            n_jobs=4
        )
    else:
        model = RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            random_state=42
        )

    model.fit(X, y)
    return model


# from xgboost import XGBRegressor

# def train_model(X, y):
#     model = XGBRegressor(
#         n_estimators=200,
#         max_depth=4,
#         learning_rate=0.05
#     )
#     model.fit(X, y)
#     return model