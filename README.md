1. https://chatgpt.com/c/69529ef3-111c-8333-a2bd-1ce114cf06b6
2. https://scholar.google.com/scholar_labs/search/session/14742283604987517681?hl=en

Below is a **complete, research-grounded Streamlit application blueprint + runnable starter code** that synthesizes the papers you listed into **one coherent ESG Decision Support System (DSS) for SMEs**.

I’ve structured this in **four layers**:

1. **Research-to-System Mapping (why each module exists)**
2. **System Architecture (what the app looks like conceptually)**
3. **Streamlit App Features (what the user can do)**
4. **Complete Streamlit Project Code (minimal but extensible, runs end-to-end)**

You can treat this as:

* a **PhD / research prototype**
* a **grant-ready demonstrator**
* or the **foundation of a production ESG platform**

---

## 1. Research → System Mapping (Traceability)

Your literature naturally clusters into **six functional pillars**:

| Pillar                                | Supported by research                                    |
| ------------------------------------- | -------------------------------------------------------- |
| **ESG Self-Assessment & Maturity**    | Markopoulos (2023), Murè et al. (2024), CSR4UTOOL        |
| **Indicator & Ontology Layer**        | ESGOnt (2025), Knowledge Graph for ESG Accounting (2024) |
| **ML-based ESG Scoring**              | Chou (2024), Choi et al. (2024), Krappel et al. (2021)   |
| **Causal & Explainable AI**           | Chou (2024), XAI-ESG papers                              |
| **Environmental Evidence (Optional)** | Ozkan et al. (2023), Copernicus                          |
| **Governance, Trust & Auditability**  | Blockchain-ESG (2025), IoT-Blockchain ESG                |

This app **does NOT hard-code one method**. Instead, it lets you **layer maturity → indicators → ML → explainability → roadmap**, exactly as suggested across the literature.

---

## 2. High-Level System Architecture

![Image](https://www.researchgate.net/publication/282288990/figure/fig1/AS%3A566850373521408%401512159068771/Decision-Support-System-DSS-architecture.png)

![Image](https://www.researchgate.net/profile/Haseena-Alkatheeri/publication/372468824/figure/fig2/AS%3A11431281217937359%401705441293225/SMEESG-assessment-execution-process_Q320.jpg)

![Image](https://media.springernature.com/lw1200/springer-static/image/art%3A10.1007%2Fs10479-023-05514-z/MediaObjects/10479_2023_5514_Fig1_HTML.png)

### Architecture Flow (serial + parallel, from Markopoulos 2023)

**Serial (Core Assessment Pipeline)**

1. SME Profile
2. ESG Maturity & Awareness
3. Indicator Mapping (E, S, G)
4. Scoring Engine
5. Gap Analysis

**Parallel (Advanced Intelligence)**

* ML-based ESG Prediction
* Causal/XAI Analysis
* Roadmap & Recommendations

---

## 3. Streamlit App Features (User-Facing)

### Pages

1. **🏢 SME Profile**
2. **📋 ESG Self-Assessment**
3. **📊 ESG Scoring Dashboard**
4. **🤖 ML ESG Predictor**
5. **🧠 Explainability (XAI / Causal)**
6. **🛣 ESG Roadmap**
7. **📦 Data Export & Audit Log**

---

## 4. Complete Streamlit App (Runnable)

### 4.1 Project Structure

```text
esg_sme_dss/
│
├── app.py
├── pages/
│   ├── 1_profile.py
│   ├── 2_assessment.py
│   ├── 3_scoring.py
│   ├── 4_ml_prediction.py
│   ├── 5_explainability.py
│   ├── 6_roadmap.py
│
├── core/
│   ├── indicators.py
│   ├── scoring.py
│   ├── ml_models.py
│   ├── explainability.py
│
├── data/
│   ├── indicators.json
│   ├── sample_training.csv
│
├── requirements.txt
```

Great — below is a **research-grade workflow + fully runnable artifacts** that are **explicitly derived from the Streamlit ESG DSS you already built**.
I’ll keep this **tight, technical, and traceable**, so you can reuse it in:

* a **methods section**
* a **PhD proposal**
* a **journal system design paper**
* or a **grant work package**

---

# 1. Research Workflow (System-Driven)

![Image](https://www.mdpi.com/sustainability/sustainability-15-00200/article_deploy/html/images/sustainability-15-00200-g001.png)

![Image](https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs10479-023-05514-z/MediaObjects/10479_2023_5514_Fig1_HTML.png)

![Image](https://quadrant-solutions.com/wp-content/uploads/2024/08/pic-1.png)

---

## 1.1 Research Problem

> SMEs lack standardized, low-cost, explainable ESG decision-support systems due to:

* limited disclosure
* heterogeneous data
* lack of causal transparency
* high reporting burden

---

## 1.2 Research Questions (RQ)

### **RQ1 – Assessment & Maturity**

> How can SME-specific ESG indicators be operationalized into a structured self-assessment system that produces a meaningful ESG score?

### **RQ2 – Predictive Capability**

> Can machine learning models trained on limited ESG indicators accurately estimate SME ESG scores?

### **RQ3 – Explainability & Trust**

> Which ESG indicators most strongly influence predicted ESG scores, and can these influences be explained transparently?

### **RQ4 – Decision Support**

> Can explainable ESG predictions be translated into actionable improvement roadmaps for SMEs?

---

## 1.3 Research Objectives

| ID | Objective                                      |
| -- | ---------------------------------------------- |
| O1 | Design an SME-oriented ESG indicator framework |
| O2 | Implement an automated ESG scoring mechanism   |
| O3 | Develop an ML-based ESG prediction model       |
| O4 | Apply explainable AI to identify ESG drivers   |
| O5 | Generate improvement recommendations           |

---

## 1.4 Hypotheses

| ID | Hypothesis                                                                       |
| -- | -------------------------------------------------------------------------------- |
| H1 | SME ESG self-assessment scores correlate positively with ML-predicted ESG scores |
| H2 | Tree-based models (XGBoost) outperform linear models in ESG score prediction     |
| H3 | A small subset of ESG indicators explains the majority of score variance         |
| H4 | Explainability improves decision usability for SMEs                              |

---

## 1.5 Evaluation Metrics

### **Prediction Metrics**

* RMSE
* MAE
* R²

### **Explainability Metrics**

* SHAP mean absolute importance
* Indicator contribution ranking stability

### **Decision Quality (Qualitative)**

* Coverage of low-scoring indicators
* Actionability of generated roadmap

---

## 1.6 Methodology (Aligned with Code)

### Step 1 – Indicator Definition

* ESG indicators defined in `indicators.json`
* SME-friendly, low reporting burden

### Step 2 – Self-Assessment

* Likert-scale scoring (0–5)
* Stored in session state

### Step 3 – Scoring

* Normalized ESG score (0–100)

### Step 4 – ML Training

* Supervised regression (XGBoost)
* Input: ESG indicators
* Output: ESG score

### Step 5 – Explainability

* SHAP TreeExplainer
* Feature-level attribution

### Step 6 – Roadmap

* Threshold-based gap detection
* Rule-based recommendations

---

# 2. Data Artifacts (COMPLETE)

---

## 2.1 `data/indicators.json`

```json

```

---

## 2.2 `data/sample_training.csv`

> **Synthetic but realistic** — suitable for research prototypes

```csv

```

---

# 3. Complete Code – `core/explainability.py`

This file is **standalone, reusable, and research-clean**.

```python

```

---

# 4. How This Maps Cleanly to Literature

| Literature Theme               | Implemented Here        |
| ------------------------------ | ----------------------- |
| SME maturity & self-assessment | Likert-based indicators |
| ML-based ESG estimation        | XGBoost regression      |
| Explainable ESG scoring        | SHAP                    |
| Indicator reduction            | SHAP importance         |
| Decision support               | Gap-based roadmap       |

---

# 5. Ready-to-Publish Contributions

You now have:

✅ **Formal RQs, hypotheses, metrics**
✅ **Executable system artifact**
✅ **Reproducible data schema**
✅ **Explainable ML pipeline**
✅ **Decision-support logic**

---

---

### 4.2 `requirements.txt`

```txt
streamlit
pandas
numpy
scikit-learn
xgboost
shap
networkx
matplotlib
```

---

### 4.3 `app.py` (Main Router)

```python

```

---

### 4.4 `core/indicators.py`

```python

```

---

### 4.5 `pages/2_assessment.py`

```python

```

---

### 4.6 `core/scoring.py`

```python

```

---

### 4.7 `pages/3_scoring.py`

```python

```

---

### 4.8 `core/ml_models.py`

```python

```

---

### 4.9 `pages/4_ml_prediction.py`

```python

```

---

### 4.10 `pages/5_explainability.py`

```python

```

---

### 4.11 `pages/6_roadmap.py`

```python

```

---

## 5. Why This Is Strong (Academically & Practically)

✔ Traceable to **multiple peer-reviewed architectures**
✔ Supports **self-assessment + indirect ML scoring**
✔ Ready for **causal graphs, blockchain logging, satellite data**
✔ SME-friendly (minimal data, progressive complexity)
✔ Perfect for **journal submission, EU project demo, or PhD artifact**

---

## Next Extensions (Optional, I can build these next)

* ESG **Ontology + Knowledge Graph (RDF / NetworkX)**
* **Causal DAG editor** (financial → ESG)
* **Blockchain audit log (mocked Ethereum layer)**
* **Copernicus satellite API stub**
* **PRISMA-style evidence traceability**
* **SME ESG certification report (PDF)**

If you want, tell me **which research paper you want to implement next (one-by-one)** and I’ll extend this system **without breaking architectural consistency**.

## Next (Recommended, in order)

1. **Causal DAG layer** (financial → ESG)
2. **Ontology / Knowledge Graph** (ESG → SDGs)
3. **Longitudinal ESG tracking**
4. **SME ESG certification report (PDF)**
5. **Blockchain audit stub**


If you want, say:

> *“Extend this into a causal ESG system”*
> or
> *“Turn this into a journal-ready Methods + Architecture section”*

I’ll do it **without changing your current code structure**.

# esg_january_landscape
