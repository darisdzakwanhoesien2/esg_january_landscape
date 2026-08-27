# Merge notes — 2026-08-28

## Context
A bulk `git pull --rebase --autostash` pulled 1 upstream commit onto `main`.
Local uncommitted work was auto-stashed and then conflicted on re-apply.
Resolved by **keeping both sides**; merged files checked with `python -m py_compile`.

## Conflicts — `pages/5_explainability.py`
| Location | Upstream had | Local had | Resolution |
|---|---|---|---|
| SHAP explainer construction | `shap.Explainer(model, X)` + a comment explaining the background distribution | `try: shap.TreeExplainer(model) except: shap.Explainer(model.predict, X)` | Kept the upstream comment **and** the local try/except (local is a strict improvement). |
| beeswarm figure render | `st.pyplot(fig); plt.close(fig)` — but `fig` was never assigned (bug) + a stale commented block | `fig = plt.gcf(); st.pyplot(fig); plt.close(fig)` | Took the local version (correct); dropped the stale commented block. |

## Also applied from the stash (no conflict)
- `pages/4_ml_prediction.py` — feature-name mapping so the assessment dict lines
  up with the trained model's feature order.
