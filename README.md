# SME ESG Decision Support System (Streamlit)

This repository contains a research-oriented **ESG Decision Support System (DSS) for SMEs** built with **Streamlit**. It includes:
- A simple **self-assessment** (Likert 0–5)
- A deterministic **ESG score** (0–100)
- An **ML-based ESG score predictor**
- **Explainability** (SHAP)
- A rule-based **improvement roadmap**
- A **research framework Sankey** view (from `data/research_framework.json`)

The previous long-form blueprint README has been preserved as `notes.md`.

---

## Quickstart

### 1) Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the app

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in your terminal.

---

## How the app works

### Pages

- `pages/2_assessment.py`: Captures SME self-assessment responses (0–5) per indicator.
- `pages/3_scoring.py`: Computes a normalized ESG score (0–100) from the assessment.
- `pages/4_ml_prediction.py`: Trains a regression model on `data/sample_training.csv` and predicts a score for the current assessment.
- `pages/5_explainability.py`: Uses SHAP to show global feature influence (beeswarm).
- `pages/6_roadmap.py`: Lists indicators with low scores (<3) as improvement gaps.
- `pages/7_research_sankey.py`: Visualizes research logic flow from `data/research_framework.json`.

### Indicator model (important)

The app uses a canonical indicator set in `core/indicators.py`:
- Labels are human-friendly (used for the UI)
- IDs are short (`E1..E3`, `S1..S3`, `G1..G3`) and are used as *feature names*

This is critical because the ML training data in `data/sample_training.csv` is columned by these IDs. The self-assessment page stores responses keyed by ID so the predictor can safely build a feature vector that matches the model.

---

## Bugs / broken logic found (and fixed)

### 1) ML feature mismatch between assessment and training data (FIXED)

**Problem**
- The self-assessment stored responses using full text labels (e.g., `"Energy consumption monitoring"`).
- The training data columns are IDs (e.g., `E1`, `E2`, …).
- That mismatch causes model input columns not to align, leading to incorrect predictions or errors depending on model backend.

**Fix**
- Updated `core/indicators.py` to define each indicator as `{id, label}`.
- Updated `pages/2_assessment.py` to store responses keyed by `id`.
- Added a defensive check in `pages/4_ml_prediction.py` that stops with a clear error if any expected feature columns are missing.

### 2) Accidental committed build artifacts (`__pycache__/*.pyc`) (FIXED)

**Problem**
- Compiled Python artifacts were tracked in git (`core/__pycache__/*.pyc`), which should not be committed.

**Fix**
- Removed tracked `*.pyc` files from git.
- Added a `.gitignore` to prevent future commits of `__pycache__/` and other common local artifacts.

---

## Code cleanup performed

- Removed redundant commented-out legacy code in `core/ml_models.py`.
- Improved readability and safety in `core/scoring.py` (type hints + empty-input guard).
- Simplified wording in `pages/4_ml_prediction.py` spinner text (the model may be XGBoost *or* RandomForest).

---

## Inline comments added (where logic is complex)

- `core/indicators.py`: Explains why indicator IDs are required for ML feature compatibility.
- `pages/2_assessment.py`: Notes that session state is stored by ID to match ML columns.
- `pages/4_ml_prediction.py`: Notes fallback model behavior + adds a “missing features” check.
- `pages/5_explainability.py`: Explains the SHAP background dataset choice at a high level.

---

## Project structure

```text
.
├── app.py
├── core/
│   ├── indicators.py
│   ├── ml_models.py
│   ├── scoring.py
│   └── explainability.py
├── data/
│   ├── indicators.json
│   ├── research_framework.json
│   └── sample_training.csv
├── pages/
│   ├── 2_assessment.py
│   ├── 3_scoring.py
│   ├── 4_ml_prediction.py
│   ├── 5_explainability.py
│   ├── 6_roadmap.py
│   └── 7_research_sankey.py
├── notes.md
├── outcome.md
└── requirements.txt
```

---

## Notes / limitations

- The ML workflow currently retrains the model on page load. If you want this to feel “production-like”, the next step is caching (`st.cache_resource`) and/or persisting a trained model artifact.
- `core/explainability.py` exists but is not wired into the Streamlit page; `pages/5_explainability.py` currently does SHAP directly. If you want, I can refactor the page to use `ESGExplainability` consistently.

---

## Project overview

SMEs are increasingly asked to report and improve ESG practices, but they often lack:
- A lightweight way to **self-assess** across E/S/G
- A transparent way to **aggregate** results into a single score
- A way to translate results into an actionable **improvement roadmap**

This project provides a Streamlit-based decision support prototype that lets an SME:
1) score itself on a small ESG indicator set (0–5 per indicator),
2) compute a normalized overall ESG score (0–100),
3) optionally run an ML model to predict an ESG score from the same indicators, and
4) view explainability (SHAP) and a basic gap-driven roadmap.

---

## Tech stack

- Language: Python 3 (tested in a local `venv`)
- UI framework: Streamlit
- Data: pandas, numpy
- ML: scikit-learn (RandomForest fallback), xgboost (preferred if installed)
- Explainability: shap
- Visualization: matplotlib (SHAP plots), plotly (Sankey), networkx (installed; currently not required by the app)

See `requirements.txt:1` for the authoritative dependency list.

---

## Architecture overview

At a high level, the app is a set of Streamlit pages that share state via `st.session_state`:

- **UI layer (`pages/*`)**
  - `pages/2_assessment.py` writes `st.session_state["assessment"]` (indicator responses).
  - `pages/3_scoring.py`, `pages/4_ml_prediction.py`, and `pages/6_roadmap.py` read from that state.
- **Core logic (`core/*`)**
  - `core/indicators.py` defines the canonical indicator set (IDs + labels).
  - `core/scoring.py` implements deterministic scoring.
  - `core/ml_models.py` trains an ML regressor (XGBoost if available, otherwise RandomForest).
- **Data (`data/*`)**
  - `data/sample_training.csv` is the training dataset for the ML predictor.
  - `data/research_framework.json` drives the Sankey diagram page.

Data flow (typical user path):
1) Assessment page → stores `{E1..G3: 0..5}` in session state
2) Scoring page → computes score from those values
3) ML page → trains on `sample_training.csv` and predicts from session state
4) Explainability page → trains + computes SHAP over the training data
5) Roadmap page → lists low-scoring indicators as “gaps”

---

## Installation & setup

### Prerequisites

- Python 3.10+ recommended (this repo works with Python 3.12 in a virtualenv)
- A working C/C++ build toolchain is **not** required if you use prebuilt wheels (typical on macOS/Linux), but large packages like `xgboost` can take time to download.

### Steps

```bash
# 1) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
python -m pip install -r requirements.txt

# 3) Run Streamlit
streamlit run app.py
```

Troubleshooting:
- If `xgboost` fails to install, the app still works: the ML module falls back to `RandomForestRegressor` automatically.

---

## Usage guide

### Basic workflow (recommended order)

1) Open the app and go to `📋 ESG Self-Assessment`
   - For each indicator, choose a value from 0 to 5.
   - The app stores responses using indicator IDs (`E1..G3`) so they match the ML dataset columns.

2) Go to `📊 ESG Score`
   - Shows the deterministic normalized score out of 100.

3) Go to `🤖 ML-Based ESG Prediction`
   - Trains a model on `data/sample_training.csv`.
   - Predicts a score for the current assessment.
   - If your assessment responses don’t match the model’s expected feature columns, the page will stop and show which columns are missing.

4) Go to `🧠 Explainability (XAI)`
   - Displays a SHAP beeswarm plot for global feature influence over the training data.

5) Go to `🛣 ESG Improvement Roadmap`
   - Lists any indicators scoring below 3 as “gaps” to improve.

### Example: What an “assessment payload” looks like

The app stores the assessment in session state as a flat dict keyed by indicator ID:

```python
{
  "E1": 4, "E2": 2, "E3": 3,
  "S1": 1, "S2": 3, "S3": 2,
  "G1": 4, "G2": 3, "G3": 2
}
```

---

## API reference (if applicable)

This repository does **not** expose a REST/HTTP API. Interaction happens via the Streamlit UI.

If you want an API later, the natural “API surface” would wrap:
- `core/scoring.compute_esg_score(responses)` → deterministic score
- `core/ml_models.train_model(X, y)` + `model.predict(input_df)` → predicted score

---

## Environment variables

No `.env` configuration is required by the current codebase.

If you later add external data sources (e.g., ESG datasets, Copernicus, company registries) or model storage, a typical `.env` might include:
- `DATA_DIR` (override data path)
- `MODEL_PATH` (persisted model location)
- `STREAMLIT_SERVER_PORT` / `STREAMLIT_SERVER_ADDRESS` (deployment configuration)

---

## Contributing guide

Contributions are welcome, especially:
- Expanding the indicator set and aligning it with a real SME framework
- Improving the roadmap logic (from simple thresholds → evidence-based recommendations)
- Adding caching/persistence for ML training (`st.cache_resource`) and model artifacts
- Wiring `core/explainability.py` into the explainability page for consistency

Suggested workflow:
1) Fork the repo
2) Create a branch for your change
3) Make changes with clear, focused commits
4) Run basic checks locally:
   - `python -m compileall -q .`
   - `streamlit run app.py`
5) Open a PR with a short problem statement and screenshots (if UI changes)

---

## License

No license file is currently included in this repository.

If you intend others to reuse/modify this code, add a `LICENSE` file (e.g., MIT, Apache-2.0, or GPL-3.0) and update this section accordingly.

---

## Scaling guide

This repository is currently a **single-process Streamlit prototype** with in-memory session state and on-demand model training. It can absolutely be deployed, but it will hit limits quickly as concurrent usage grows.

### 1) Current bottlenecks (what breaks first under load)

- **Per-user recomputation**: pages like `pages/4_ml_prediction.py` and `pages/5_explainability.py` train a model / compute SHAP at runtime. Under concurrent usage, CPU time will spike and response times will degrade.
- **SHAP cost**: SHAP can be expensive (especially for larger datasets). It will become the first “CPU burner” as your dataset grows or if many users open the explainability page.
- **No caching/persistence**: nothing is cached across sessions (no `st.cache_resource` for model objects; no model artifact saved to disk/object storage).
- **Single instance constraints**: a single Streamlit server is limited by one machine’s CPU/RAM. Scaling it without a shared backend leads to inconsistent behavior (e.g., caching per instance).
- **Data loading pattern**: reading `data/sample_training.csv` on each page load is fine for small files, but becomes wasteful if you swap in real datasets.
- **State storage**: `st.session_state` is per-session, in-memory. It’s not durable and doesn’t support multi-instance consistency.

### 2) Database scaling (indexing, caching, sharding, read replicas)

Today the app has **no database**. If you evolve it into a production system, the typical data you’ll want to store includes:
- Users/orgs (SME profiles)
- Assessments (per date/period)
- Generated scores + predictions
- Model versions/metadata
- Audit logs and exports

Recommended baseline (MVP → production):
- **Primary DB**: PostgreSQL (managed)
  - Tables: `orgs`, `users`, `assessments`, `assessment_items`, `scores`, `predictions`, `model_versions`, `audit_events`
  - Indexes:
    - `assessments(org_id, created_at)`
    - `assessment_items(assessment_id, indicator_id)`
    - `predictions(org_id, created_at, model_version)`
  - Use JSONB cautiously; prefer normalized rows for queries/analytics.
- **Caching**: Redis
  - Cache “hot” reads (latest assessment, score summaries)
  - Rate-limit expensive operations (e.g., explanation jobs)
- **Read replicas**: add when read-heavy (dashboards) outgrow primary.
- **Partitioning (before sharding)**:
  - Partition large time-series tables by month/quarter (e.g., `assessments`).
- **Sharding**:
  - Usually not needed until very large scale; if needed, shard by `org_id` with application-level routing.

### 3) Backend scaling (load balancing, horizontal vs vertical scaling)

Streamlit is a great UI layer, but it’s not the best place to run long-lived heavy compute for many concurrent users.

Recommended architecture split:
- **Frontend/UI**: Streamlit (stateless where possible)
- **Backend API**: FastAPI (or similar) for persistence and compute orchestration
- **Async jobs**: background workers for training/explainability (Celery/RQ/Arq) + a queue (Redis/SQS)

Scaling tactics:
- **Vertical scaling (early)**: bigger instance for Streamlit if concurrency is low (simple and cheap initially).
- **Horizontal scaling (later)**: multiple Streamlit instances behind a load balancer
  - Requires shared backing services (DB/Redis/object storage) so instances remain interchangeable.
- **Load balancing**:
  - Use an L7 load balancer (ALB/Cloud Run/Ingress) with health checks.
  - Avoid per-instance local state; treat instances as disposable.
- **Compute isolation**:
  - Move model training + SHAP to background jobs; Streamlit triggers jobs and polls results.

### 4) Frontend scaling (CDN, lazy loading, SSR/SSG options)

This project’s “frontend” is Streamlit, not a traditional SPA/SSR app. Still, you can improve perceived performance:
- **CDN**: put a CDN/edge in front of the app for static assets and TLS termination (CloudFront / Cloud CDN / Azure Front Door).
- **Lazy loading (conceptual)**:
  - Don’t compute SHAP until the user explicitly requests it (button-driven).
  - Prefer “summary first”: show top features (fast) then offer full beeswarm (slow).
- **SSR/SSG**:
  - Not directly applicable to Streamlit. If you need SEO/public marketing pages, host a separate static site (Next.js, Astro) and link to the app.

### 5) Infrastructure recommendations (AWS / GCP / Azure)

Below are three “production-shaped” options; pick based on team familiarity.

**AWS (common enterprise default)**
- Compute: ECS Fargate (Streamlit + API) or EKS (if you already run Kubernetes)
- Load balancing: ALB
- DB: RDS PostgreSQL (+ read replica later)
- Cache/queue: ElastiCache Redis (cache + job broker) or SQS for queue + Redis for cache
- Object storage: S3 (exports, model artifacts)
- Observability: CloudWatch + X-Ray (or OpenTelemetry to Grafana/Datadog)
- Secrets: Secrets Manager / SSM Parameter Store

**GCP (great for managed + simple ops)**
- Compute: Cloud Run (Streamlit + API containers)
- Load balancing: Cloud Load Balancing (or Cloud Run ingress)
- DB: Cloud SQL for PostgreSQL
- Cache: Memorystore (Redis)
- Queue: Pub/Sub or Cloud Tasks
- Storage: Cloud Storage (GCS)
- Observability: Cloud Logging/Monitoring + Trace
- Secrets: Secret Manager

**Azure**
- Compute: Container Apps (or AKS if you need Kubernetes)
- Load balancing: Front Door / Application Gateway
- DB: Azure Database for PostgreSQL
- Cache: Azure Cache for Redis
- Queue: Service Bus
- Storage: Blob Storage
- Observability: Azure Monitor / Application Insights
- Secrets: Key Vault

### 6) Cost estimate (rough; 1k / 10k / 100k users)

These are intentionally **order-of-magnitude** estimates because real cost depends on:
- concurrent users (not total users),
- how often users run ML/SHAP,
- dataset size,
- and how much you cache/precompute.

Assumptions for ballpark sizing:
- 1k / 10k / 100k **monthly active users**
- Peak concurrency roughly 1% of MAU (10 / 100 / 1,000 concurrent)
- Heavy compute pages (ML/SHAP) are used by a minority; in production they run as async jobs.

**1k users (small pilot) — ~$50–$200/month**
- 1 small container instance for Streamlit (or Cloud Run min instances = 0)
- Managed Postgres (small)
- Minimal storage/logging

**10k users (growing) — ~$300–$1,500/month**
- 2–4 app instances behind LB (Streamlit + API)
- RDS/CloudSQL sized up, maybe a small read replica
- Redis cache
- Background worker for jobs

**100k users (serious usage) — ~$2,000–$15,000+/month**
- Many stateless app instances + autoscaling
- DB with read replicas + partitioning; possibly dedicated analytics store later
- Redis cluster
- Job queue + multiple workers (explainability/training)
- CDN + increased egress/logging

To make costs predictable at scale, prioritize:
- caching, async jobs, precomputation,
- and reducing SHAP frequency (or using cheaper explanation summaries).

### 7) Roadmap: MVP → production-grade scaling path

**Phase 0 (now): prototype hygiene**
- Add caching where safe: `st.cache_data` for loading datasets; `st.cache_resource` for model objects.
- Ensure feature alignment stays strict (already guarded in `pages/4_ml_prediction.py`).
- Add basic logging around expensive operations (train, explain).

**Phase 1 (MVP deployment): single instance**
- Deploy Streamlit as one container (Cloud Run / ECS / Container Apps).
- Add a real DB (Postgres) only if you need persistence; otherwise keep it stateless.
- Add basic monitoring (request latency, CPU/RAM).

**Phase 2 (early scale): split UI and backend**
- Introduce a FastAPI backend:
  - persist assessments and scores,
  - provide a stable “scoring/prediction” interface,
  - version model artifacts.
- Store artifacts and exports in object storage (S3/GCS/Blob).

**Phase 3 (growth): async compute + cache**
- Move training/explainability to background jobs (queue + workers).
- Add Redis:
  - cache hot reads,
  - broker jobs (or keep queue managed and use Redis purely for cache).
- Introduce rate limits / quotas to protect expensive operations.

**Phase 4 (production): HA + cost controls**
- Multiple instances behind a load balancer with autoscaling.
- DB read replicas; partition large tables; tune indexes based on real queries.
- CDN in front for TLS/edge + static assets.
- Security hardening:
  - secrets manager,
  - least-privilege IAM,
  - audit logs,
  - backups + disaster recovery plan.

**Phase 5 (enterprise scale): analytics + governance**
- Separate OLTP (Postgres) from analytics (BigQuery/Redshift/Snowflake).
- Add model monitoring (data drift, performance metrics).
- Implement tenant isolation rules (per org) and compliance controls.

---

## Competitive landscape (10 comparable products) + differentiation ideas

The ESG software space is broad. The closest “adjacent” products to this project tend to fall into one (or more) of these categories:
- **Supplier ESG ratings / questionnaires** (supply chain risk + procurement enablement)
- **ESG reporting and disclosure** (audit-ready reporting for frameworks/regulators)
- **Carbon accounting / climate management** (Scope 1–3 measurement, reduction planning, supplier engagement)
- **Materiality and regulatory monitoring** (policy + obligations tracking)

Important note on “tech stack”: many vendors do not publicly disclose their detailed implementation stacks. Where stack details aren’t public, this section lists **observable/declared product capabilities** (e.g., “AI platform”, “API access”, “SaaS”, “SHAP/XAI is not mentioned”, etc.).

### 1) EcoVadis (supplier sustainability ratings)

- What they do: Supplier sustainability ratings and scorecards for companies; large network of rated companies. EcoVadis reports 150,000+ rated companies.  
- Tech stack (if known): Not publicly disclosed; operates a web-based platform and references ML usage in methodology disclosures.  
- Business model: Subscription for ratings/solutions.  
- Scale (public indicators): 150,000+ rated companies.  
- Why successful:
  - Strong distribution via procurement/supply-chain requirements (“your customer demands an EcoVadis rating” loop).
  - Standardized questionnaires and benchmarks at global network scale.
  - Clear outputs that map well to procurement workflows (scorecards, medals/badges).

Sources: EcoVadis company info / scale. https://ecovadis.com/about-us/ citeturn5search1

### 2) Workiva (ESG + financial/regulatory reporting)

- What they do: Cloud platform for connected reporting workflows (SEC, financial, and sustainability/ESG reporting in one platform).  
- Tech stack (if known): Not publicly disclosed; positioned as a cloud platform with AI capabilities.  
- Business model: Subscription SaaS (public company).  
- Scale (public indicators): Widely adopted in regulated reporting; large enterprise footprint (see company materials).  
- Why successful:
  - Deep entrenchment in regulated reporting workflows and controls.
  - Collaboration + audit trail + data lineage as core product strengths.
  - Strong switching costs once reporting is standardized.

Sources: Workiva SEC reporting overview. https://www.workiva.com/solutions/sec-reporting citeturn0search2

### 3) Persefoni (carbon accounting + climate disclosure)

- What they do: Carbon accounting and sustainability management platform (Scope 1–3), reporting, and disclosure support.  
- Tech stack (if known): Not publicly disclosed; offers API access on higher tiers and positions itself as enterprise-grade.  
- Business model: Tiered SaaS subscriptions (including a free/pro tier on their pricing page, plus paid tiers).  
- Scale (public indicators): Public customer case studies exist (customer list is published).  
- Why successful:
  - Strong positioning around disclosure readiness and enterprise-grade assurance/security.
  - Clear value proposition for complex Scope 3 programs and supplier data collection.

Sources: Persefoni pricing and customers pages. https://www.persefoni.com/pricing and https://www.persefoni.com/en-gb/customers citeturn0search0turn5search2

### 4) Watershed (enterprise climate platform)

- What they do: Enterprise climate platform for measuring, reporting, and reducing emissions; publishes customer stories and highlights a sizable team.  
- Tech stack (if known): Not publicly disclosed; marketed as a software platform with large emissions factor coverage and climate expertise embedded.  
- Business model: Enterprise SaaS (typical for this category).  
- Scale (public indicators): “Nearly 400 people” and customer examples listed on their site.  
- Why successful:
  - Strong enterprise go-to-market, services + software, and credible climate expertise.
  - Focus on end-to-end programs (measurement → planning → action) vs “just reporting”.

Sources: Watershed “About us” + customer page. https://watershed.com/about-us and https://watershed.com/fr/customers citeturn5search0turn5search6

### 5) Sweep (enterprise carbon management)

- What they do: Carbon management platform aimed at larger enterprises (Scope 1–3, value chain, reporting).  
- Tech stack (if known): Not publicly disclosed.  
- Business model: Enterprise SaaS.  
- Scale (public indicators): Significant venture funding and named enterprise customers in public materials.  
- Why successful:
  - Strong positioning for enterprise Scope 3 and supply-chain collaboration.
  - Funding enables faster product and go-to-market expansion.

Sources: Sweep Series B press release. https://www.businesswire.com/news/home/20220404005766/en/Climate-Tech-Firm-Sweep-Raises-%2473-Million-in-Series-B-Funding-Led-by-Coatue citeturn3search1

### 6) Plan A (decarbonization + ESG platform)

- What they do: Carbon accounting + ESG reporting platform; European footprint and notable customers mentioned in press.  
- Tech stack (if known): Not publicly disclosed; described as an “AI-powered” platform in some public materials.  
- Business model: SaaS; offers API integration per reporting.  
- Scale (public indicators): Reported 1,500+ clients in a funding press release; raised $27M Series A reported in press.  
- Why successful:
  - Clear European regulatory narrative (CSRD and related reporting needs).
  - Customer and partner momentum in a compliance-driven market.

Sources: Demeter press release and TechCrunch coverage. https://demeter-im.com/wp-content/uploads/ENG_230919_Press-release_Plan-A_Funding.pdf and https://techcrunch.com/2023/09/19/plan-a-carbon-accounting/ citeturn2search4turn2search14

### 7) Greenly (carbon accounting SaaS)

- What they do: Carbon accounting SaaS platform (B2B) for measuring and managing footprints; has public funding coverage.  
- Tech stack (if known): Not publicly disclosed; marketed as a SaaS platform.  
- Business model: Subscription SaaS (typical).  
- Scale (public indicators): Public funding coverage and broad business adoption; exact customer counts vary by source.  
- Why successful:
  - Clear mid-market-friendly positioning (carbon accounting made simpler).
  - Strong packaging around “measure → reduce → report” with guidance and integrations.

Sources: Wikipedia overview and third-party funding summaries. https://en.wikipedia.org/wiki/Greenly_(company) citeturn2search12

### 8) Normative (carbon accounting “engine”)

- What they do: Carbon accounting platform/engine emphasizing transparent calculations and emissions factor depth.  
- Tech stack (if known): Not publicly disclosed; positions itself as an engine with APIs and a large emissions-factor dataset.  
- Business model: SaaS subscription (typical).  
- Scale (public indicators): Funding press materials mention “hundreds of customers”.  
- Why successful:
  - Strong product story around transparency and standards alignment.
  - “Engine” positioning fits embedding in larger ecosystems (partners, integrations).

Sources: Normative platform page and press release PDF. https://normative.io/platform/ and https://normative.io/wp-content/uploads/2021/10/Press-release-Emissions-accounting-engine-Normative-raises-E10-million-from-Europes-largest-climate-tech-funds.pdf citeturn3search0turn3search13

### 9) Sphera (enterprise sustainability + EHS/operational risk)

- What they do: Enterprise sustainability + operational risk/EHS software; broad suite with large customer base.  
- Tech stack (if known): Not publicly disclosed; marketed as SaaS platform (SpheraCloud).  
- Business model: Enterprise software + services (subscription/licensing + implementation).  
- Scale (public indicators): Sphera states 8,400+ customers on its website.  
- Why successful:
  - Very strong enterprise fit in heavy/regulated industries (EHS + sustainability).
  - Platform breadth and long operating history.

Sources: Sphera site (customer count) and product positioning. https://sphera.com/ citeturn4search3

### 10) Datamaran (ESG regulatory monitoring + materiality)

- What they do: AI platform for ESG regulatory monitoring and materiality/risk insights (“smart way to ESG”).  
- Tech stack (if known): Not publicly disclosed; described as an AI platform.  
- Business model: Subscription SaaS (typical).  
- Scale (public indicators): Company describes a team of 120+ ESG experts/data scientists/etc.  
- Why successful:
  - Clear niche: continuously monitoring a rapidly changing regulatory landscape.
  - Strong “signal extraction” value proposition (reduce manual scanning/research).

Sources: Datamaran site + about page. https://www.datamaran.com/ and https://www.datamaran.com/about-us citeturn4search0turn5search5

---

## What could differentiate *this* project (niche ideas)

Most successful ESG SaaS products win on **distribution**, **compliance trust**, and **workflow lock-in**. Your strongest “niche” opportunities are likely where large vendors are weakest or overpriced:

1) **SME-first UX + low reporting burden**
   - Optimize for minimal data entry, guided flows, and “good enough” evidence capture.
   - Make “first ESG score in 15 minutes” a product promise.

2) **Open, transparent scoring + explainability**
   - Many ESG platforms are perceived as “black boxes”. A transparent, research-grounded scoring and explanation layer can build trust.
   - Lean into reproducibility: clearly define indicator weights, scoring logic, and versioning.

3) **Audit-friendly outputs for a *specific* standard**
   - Pick a narrow initial compliance target and do it extremely well (e.g., a CSRD/ESRS-ready SME pack, or a supply-chain questionnaire export aligned to common customer requests).

4) **Supplier-chain “response pack” generator**
   - SMEs often face repeated ESG/CO2 requests from larger customers. A killer niche is automating reusable response packs:
     - standardized answers,
     - evidence attachments,
     - structured exports (CSV/XLSX/JSON).

5) **Privacy-first / self-hosted option**
   - A meaningful niche (especially for SMEs) is providing a self-hostable version or “bring-your-own-cloud” deployment for sensitive data.

6) **Explainability that leads directly to actions**
   - The gap between “here’s a SHAP plot” and “here’s what to do next week” is huge.
   - Invest in decision support: prioritized actions, effort/impact estimates, and roadmap tracking.

If you tell me your target market (region + industry + whether you care more about **carbon** vs broader **ESG** vs **supplier questionnaires**), I can rewrite this section into a focused go-to-market positioning statement and a concrete feature moat.

### “All of it” strategy (how to cover ESG + carbon + compliance + questionnaires)

If your goal is to cover the full surface area (ESG scoring + carbon accounting + disclosure readiness + supplier questionnaires), the safest way to avoid becoming a “bloated tool” is to keep the product **modular**:

- **Module A — SME ESG self-assessment + scoring (this repo today)**
  - Fast onboarding, minimal fields, transparent scoring.
- **Module B — Carbon accounting**
  - Start with a pragmatic baseline (Scope 1–2) and add Scope 3 categories gradually.
  - Provide a clear emissions-factor provenance and versioning story.
- **Module C — Disclosure / compliance exports**
  - Don’t attempt to support every framework at once.
  - Implement “export packs” (CSV/XLSX/PDF) that map your internal indicator model to selected standards.
- **Module D — Supplier questionnaire response packs**
  - Provide a reusable knowledge base + evidence vault so SMEs can respond once and reuse across customers.

**Positioning that can win against bigger suites**

Big suites often win on breadth, but SMEs frequently need: (1) speed, (2) clarity, (3) affordability, and (4) reusability of answers/evidence.

This project can carve out a durable niche by being:
- **SME-first**: “first credible ESG + carbon snapshot in under an hour”
- **transparent**: open scoring logic + explainability; version every indicator/model change
- **export-native**: one-click “customer pack” exports and audit trails (not just dashboards)
- **privacy-flexible**: offer SaaS + self-host / “bring your own cloud” for sensitive customers

**Feature moat ideas (practical, defensible)**

1) **Canonical data model**: a stable internal schema that maps to multiple outputs (questionnaires + disclosures).
2) **Evidence vault**: attachments + links + provenance + expiry reminders (turns “ESG” into a repeatable workflow).
3) **Change tracking**: indicator/version diffs that explain “why your score changed”.
4) **Actionability loop**: roadmap items become tasks with owners/dates; track progress and re-score.
5) **SME benchmark baselines**: lightweight peer comparisons by sector/size (even if initially coarse).

**Go-to-market wedge without losing the “all” vision**

Even if the endgame is “all of it”, pick one entry wedge first:
- “Supplier response packs” (high pain, immediate ROI), or
- “CSRD/ESRS-lite pack for SMEs” (compliance pull in EU), or
- “Scope 1–2 + top Scope 3 categories” (climate programs).

Then expand modules behind a consistent schema and export system.

---

## 6–12 month execution roadmap (milestones + data model + storage + API + deployment)

This roadmap assumes you want to evolve the current Streamlit prototype into a production-shaped system that supports:
- ESG self-assessment + scoring
- Carbon accounting (incremental)
- Disclosure/export packs
- Supplier questionnaire response packs

It’s written to be **modular**: each phase delivers a usable product slice without blocking later expansion.

### Guiding principles (to avoid “doing everything at once”)

- **One canonical schema** internally; everything else is a view/export.
- **Move compute out of Streamlit** as soon as it’s expensive (training, SHAP, report generation).
- **Async for heavy jobs**, cached for repeatable results.
- **Version everything** (indicator definitions, scoring rules, model artifacts, emissions factors).

---

### Phase 0 (Weeks 1–2): Production hygiene + schema foundation

**Milestones**
- Add app-level caching:
  - `st.cache_data` for loading datasets
  - `st.cache_resource` for model objects (short-lived)
- Add basic observability hooks (structured logs around: scoring, training, explainability)
- Freeze a canonical indicator schema (IDs + labels + metadata)
- Define a versioning policy:
  - `indicator_set_version`
  - `scoring_version`
  - `model_version`

**Data model (draft)**
- `Indicator {id, pillar, label, description?, active, version}`
- `IndicatorSet {version, created_at, notes}`

**Storage**
- Still file-based (`data/*`) for MVP, but align to a future DB schema.

**Deployment**
- Keep local-only; optional single-instance deploy for demos.

---

### Phase 1 (Month 1–2): Persisted assessments + “export pack” MVP

Goal: make it **useful for a real SME** by persisting assessments and generating reusable outputs.

**Milestones**
- Introduce a backend API (FastAPI recommended) to persist:
  - org profile, assessments, scores
- Implement “Export Pack v1”:
  - assessment summary + score + gaps (CSV/XLSX + PDF/HTML)
- Add authentication (start simple):
  - passwordless email magic link OR OAuth (Google/Microsoft) for pilot users

**Data model (minimum viable)**
- `Org {id, name, industry, size_band, country, created_at}`
- `User {id, org_id, email, role, created_at}`
- `Assessment {id, org_id, period_start, period_end, created_at, indicator_set_version}`
- `AssessmentItem {assessment_id, indicator_id, value_0_5}`
- `Score {assessment_id, score_0_100, scoring_version, computed_at}`
- `AuditEvent {id, org_id, user_id?, action, payload_json, created_at}`

**Storage choices**
- Primary DB: PostgreSQL (managed)
- Object storage: S3/GCS/Azure Blob for exports (PDF/XLSX)
- Optional cache: Redis (can wait until Phase 2 if usage is low)

**API endpoints (v1)**
- `POST /v1/orgs` → create org
- `POST /v1/users` → invite user (or handled by auth provider)
- `GET /v1/indicators` → return active indicator set + version
- `POST /v1/assessments` → create assessment header
- `PUT /v1/assessments/{assessment_id}/items` → upsert item values
- `POST /v1/assessments/{assessment_id}/score` → compute deterministic score
- `POST /v1/assessments/{assessment_id}/exports` → generate export pack (sync for now)
- `GET /v1/assessments/{assessment_id}` → fetch assessment + items + score

**Deployment plan**
- Start with a single environment:
  - Streamlit UI container + FastAPI container
  - Managed Postgres
  - Object storage bucket
- Keep it simple: 1–2 instances behind a managed ingress.

---

### Phase 2 (Month 3–4): Carbon accounting “baseline” + evidence vault

Goal: add the two biggest adoption accelerators for SMEs:
1) basic carbon footprinting and
2) evidence collection/reuse.

**Milestones**
- Implement carbon “baseline” module:
  - Scope 1–2 first (stationary combustion + purchased electricity)
  - Add a few high-impact Scope 3 categories (e.g., business travel, purchased goods) later
- Add an Evidence Vault:
  - upload documents, link URLs, tag to indicators
  - expiry/reminder metadata (optional)
- Add “Questionnaire Pack v1”:
  - generate reusable answers from saved evidence + latest assessment

**Data model additions**
- `Evidence {id, org_id, name, kind, storage_uri, source_url?, uploaded_at, expires_at?}`
- `EvidenceLink {evidence_id, indicator_id, note?}`
- `EmissionFactor {id, source, region, unit, value, valid_from, valid_to, version}`
- `ActivityData {id, org_id, period_start, period_end, activity_type, amount, unit, metadata_json}`
- `EmissionsResult {id, org_id, period_start, period_end, scope, category, tco2e, factor_version, computed_at}`

**Storage**
- DB: Postgres for metadata
- Blob storage: evidence files + generated packs
- Cache: Redis begins to pay off (hot reads + rate limiting)

**API endpoints (v2 additions)**
- `POST /v1/evidence` (multipart upload) → returns `evidence_id`
- `POST /v1/evidence/{id}/link` → link evidence to indicator(s)
- `POST /v1/carbon/activity` → submit activity data
- `POST /v1/carbon/compute` → compute emissions results (can be sync at small scale)
- `GET /v1/carbon/results?period=...` → retrieve emissions summary

**Deployment**
- Same as Phase 1, but ensure blob storage + signed URLs for uploads/downloads.

---

### Phase 3 (Month 5–6): ML + explainability as async jobs + model registry

Goal: make ML/explainability reliable under load and auditable.

**Milestones**
- Move ML training/prediction and SHAP generation to background jobs:
  - job queue + workers
  - job status + result storage
- Add a simple Model Registry:
  - store model artifacts + metadata + metrics
  - enable rollbacks by version
- Add evaluation metrics (RMSE/MAE/R²) logged per model version

**Data model additions**
- `Job {id, org_id, type, status, created_at, started_at?, finished_at?, error?}`
- `JobResult {job_id, payload_json, storage_uri?}`
- `ModelVersion {id, kind, created_at, training_data_ref, metrics_json, artifact_uri}`
- `Prediction {id, assessment_id, model_version_id, predicted_score_0_100, created_at}`
- `Explanation {id, model_version_id, kind, artifact_uri, created_at}` (e.g., SHAP summary)

**Storage**
- Redis: queue broker / caching
- Blob storage: model artifacts, explanation artifacts, large exports

**API endpoints (v3 additions)**
- `POST /v1/models/train` → returns `job_id`
- `POST /v1/models/{model_version}/predict` → returns `job_id` (or sync for small payloads)
- `POST /v1/models/{model_version}/explain` → returns `job_id`
- `GET /v1/jobs/{job_id}` → status
- `GET /v1/jobs/{job_id}/result` → outputs (or signed URL)

**Deployment**
- Add a worker service:
  - `api` service + `worker` service + `streamlit` service
  - autoscale workers separately from UI/API

---

### Phase 4 (Month 7–9): Multi-tenant hardening + performance + compliance exports

Goal: “production-grade” for multiple SMEs with predictable performance and strong exports.

**Milestones**
- Tenant isolation rules enforced everywhere (`org_id` scoping)
- Role-based access control (RBAC) for org admins vs members
- Caching strategy:
  - cache “latest assessment summary” and “dashboard aggregates”
- Add disclosure mapping packs (choose 1–2 to do well first):
  - e.g., CSRD/ESRS-lite SME pack or a common supply-chain questionnaire template

**Data model additions**
- `Role {id, name}`
- `UserRole {user_id, org_id, role_id}`
- `DisclosurePack {id, org_id, standard, version, created_at, artifact_uri}`

**API endpoints**
- `POST /v1/disclosures/generate` → returns `job_id`
- `GET /v1/disclosures/{id}` → metadata + download URL

**Deployment**
- Separate environments:
  - `dev`, `staging`, `prod`
- Add CI checks:
  - linting, type checks (optional), smoke tests
- Add backups + retention policies for DB and object storage

---

### Phase 5 (Month 10–12): Scale + analytics + enterprise readiness

Goal: scale safely and become “enterprise-ready” where needed.

**Milestones**
- Horizontal scaling for UI/API behind an L7 load balancer
- Read replica for Postgres if dashboards become read-heavy
- Partition large tables by time for performance
- Analytics pipeline (optional but powerful):
  - export event + assessment data to a warehouse (BigQuery/Redshift/Snowflake)
- Model monitoring:
  - drift checks, metric tracking per org/industry segment

**Deployment plan (cloud-agnostic)**
- Compute: containerized services (`streamlit`, `api`, `worker`)
- Ingress/LB: HTTPS termination + health checks + autoscaling
- DB: managed Postgres + backups + read replica
- Cache/queue: managed Redis (or managed queue + Redis cache)
- Storage: object storage for artifacts and evidence, with signed URLs
- Secrets: managed secrets store
- Observability: centralized logs + metrics + traces (OpenTelemetry recommended)

---

### Recommended “final shape” (target architecture)

- **Streamlit UI**: purely presentation + calling APIs; minimal compute
- **API service**: authentication/authorization, persistence, orchestration
- **Worker service**: ML training, SHAP/explanations, report generation
- **Postgres**: system of record
- **Redis/Queue**: async jobs + caching
- **Object storage**: evidence + exports + model/explanation artifacts

If you want, I can also:
- add an `openapi.yaml` stub aligned to the endpoints above, or
- scaffold a `backend/` FastAPI service + `docker-compose.yml` so the repo starts moving toward Phase 1 immediately.
