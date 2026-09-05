<div align="center">

<img src="assets/logo.jpg" alt="RazorSentinel-AI Logo" width="600" style="border-radius:8px;"/>

<br/>

<img src="https://img.shields.io/badge/🛡️_RazorSentinel--AI-Chargeback_Defense-0d1526?style=for-the-badge&labelColor=050914" alt="RazorSentinel-AI"/>

<br/><br/>

[![Live Demo](https://img.shields.io/badge/⚡_Live_Dashboard-Render-4f8ef7?style=for-the-badge&logo=render&logoColor=white)](https://razorsentinel-ai.onrender.com)
[![Landing Page](https://img.shields.io/badge/🌐_Landing_Page-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://razorsentinel-ai.vercel.app)
[![GitHub](https://img.shields.io/badge/⎇_Source_Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI)

<br/>

[![Track](https://img.shields.io/badge/Track_02-AI_Risk_Manager-6366f1?style=for-the-badge)](.)
[![Defense Only](https://img.shields.io/badge/Architecture-Defense_Only_✅-10b981?style=for-the-badge)](.)
[![PR-AUC](https://img.shields.io/badge/PR--AUC-0.7519-f59e0b?style=for-the-badge)](.)
[![Recall](https://img.shields.io/badge/Recall-90.2%25-22d3ee?style=for-the-badge)](.)
[![Hallucinations](https://img.shields.io/badge/Claims-Grounded-ef4444?style=for-the-badge)](.)

<br/><br/>

# 🛡️ RazorSentinel-AI

### *Autonomous Chargeback Verifier & Evidence Responder*

**Razorpay AI Buildathon 2026 · Track 02: AI Risk Manager**

> Stop the merchant losing money to chargebacks — with an autonomous two-stage system that verifies disputes and generates evidence-grounded defense packets, mathematically guaranteeing the removal of unsupported claims.

</div>

---

## 🎥 Video Demo & Screenshots

**Watch the full 5-minute pitch and demo:**  
<a href="https://www.youtube.com/watch?v=dAWx58ywIFE">
  <img src="https://img.youtube.com/vi/dAWx58ywIFE/maxresdefault.jpg" width="800" alt="RazorSentinel-AI Pitch Video">
</a>

<br/>

### 📸 Application Gallery

<details>
<summary><b>Click to expand and view all 21 interface screenshots</b></summary>

<br/>

<table>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_01.png" alt="Screenshot 1"></td>
    <td width="33%"><img src="Project%20demo/screenshot_02.png" alt="Screenshot 2"></td>
    <td width="33%"><img src="Project%20demo/screenshot_03.png" alt="Screenshot 3"></td>
  </tr>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_04.png" alt="Screenshot 4"></td>
    <td width="33%"><img src="Project%20demo/screenshot_05.png" alt="Screenshot 5"></td>
    <td width="33%"><img src="Project%20demo/screenshot_06.png" alt="Screenshot 6"></td>
  </tr>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_07.png" alt="Screenshot 7"></td>
    <td width="33%"><img src="Project%20demo/screenshot_08.png" alt="Screenshot 8"></td>
    <td width="33%"><img src="Project%20demo/screenshot_09.png" alt="Screenshot 9"></td>
  </tr>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_10.png" alt="Screenshot 10"></td>
    <td width="33%"><img src="Project%20demo/screenshot_11.png" alt="Screenshot 11"></td>
    <td width="33%"><img src="Project%20demo/screenshot_12.png" alt="Screenshot 12"></td>
  </tr>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_13.png" alt="Screenshot 13"></td>
    <td width="33%"><img src="Project%20demo/screenshot_14.png" alt="Screenshot 14"></td>
    <td width="33%"><img src="Project%20demo/screenshot_15.png" alt="Screenshot 15"></td>
  </tr>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_16.png" alt="Screenshot 16"></td>
    <td width="33%"><img src="Project%20demo/screenshot_17.png" alt="Screenshot 17"></td>
    <td width="33%"><img src="Project%20demo/screenshot_18.png" alt="Screenshot 18"></td>
  </tr>
  <tr>
    <td width="33%"><img src="Project%20demo/screenshot_19.png" alt="Screenshot 19"></td>
    <td width="33%"><img src="Project%20demo/screenshot_20.png" alt="Screenshot 20"></td>
    <td width="33%"><img src="Project%20demo/screenshot_21.png" alt="Screenshot 21"></td>
  </tr>
</table>

</details>

---

## 📋 Table of Contents

- [Video Demo & Screenshots](#-video-demo--screenshots)
- [What It Solves](#-what-it-solves)
- [Razorpay Integration Boundary](#-razorpay-integration-boundary)
- [Architecture](#-architecture)
- [Train/Validation/Test Methodology](#-trainvalidationtest-methodology)
- [Evaluation Metrics](#-evaluation-metrics--held-out-test-set)
- [Cost-Weighted Thresholding](#-cost-weighted-thresholding)
- [Defense-Only Guarantee](#-defense-only-guarantee)
- [Anti-Leakage Design](#-anti-leakage-evaluation-design)
- [Repo Structure](#-repository-structure)
- [Quickstart & Reproducibility](#-quickstart--reproducibility)
- [Tech Stack](#-tech-stack)
- [What Broke](#-what-broke-and-how-we-got-out)
- [Rubric Alignment](#-rubric-alignment)

---

## 🎯 What It Solves

Merchants lose money on chargebacks **twice**:

1. **First loss** — when the dispute is filed and the transaction amount is reversed
2. **Second loss** — when the merchant fails to respond with compelling evidence in time

**Single loss class targeted:** Chargebacks & Disputes (exactly as required by the rubric — one class, measured deeply).

RazorSentinel-AI eliminates the second loss by automatically:
- **Verifying** each incoming dispute: is it winnable?
- **Responding** for winnable disputes with a structured, evidence-grounded defense packet, ensuring unsupported evidence assertions are prevented from reaching the final packet.

---

## 💳 Razorpay Integration Boundary

RazorSentinel is designed around Razorpay payment and dispute evidence workflows.

- The ML evaluation dataset is **synthetic** because real chargeback data is unavailable for public training/evaluation.
- Razorpay-specific transaction identifiers and payment context are represented through the evidence schema.
- No claim is made that the demo has access to production Razorpay dispute data. 

This strict separation ensures academic and technical safety while demonstrating a pipeline built specifically for the Razorpay ecosystem.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         INCOMING DISPUTE                                 │
│        (Reason Code + AVS/CVV + Device Trust + IP/Geo + Delivery)       │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    STAGE 1 — LightGBM VERIFIER                           │
│                                                                          │
│  Features: 11 structured evidence fields                                 │
│  • AVS Match         • CVV Match          • Device Trust Score (0–1)    │
│  • IP/Geo Match      • Delivery Confirmed • Is Digital Good              │
│  • Customer History  • Prior Disputes     • Transaction Amount           │
│  • Reason Code       • Confounder (noise) ← proves model generalises    │
│                                                                          │
│  Output: Win probability P(win | evidence)                               │
│  Threshold: 0.29  (cost-optimal, NOT a default)                          │
│                                                                          │
│  Metric: PR-AUC 0.7519 on 10,000 held-out records                       │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                     if P > 0.29 (DEFENSIBLE)
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   STAGE 2 — GEMINI AUTO-RESPONDER                        │
│                                                                          │
│  Input:  DisputeEvidence (Pydantic model — strictly typed)               │
│  Output: DefensePacket   (Pydantic model — Optional[bool] fields)        │
│                                                                          │
│  LLM constraints:                                                        │
│  • No free-form prose — must fill a fixed Boolean field schema           │
│  • Temperature = 0.0  — deterministic output                             │
│  • response_mime_type = "application/json" — structured only             │
│                                                                          │
│  Post-generation Python guardrail:                                       │
│  • Every LLM assertion checked against source evidence                   │
│  • Unverified claim → None (omitted), NEVER flipped to False             │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    DEFENSE PACKET JSON OUTPUT                            │
│                                                                          │
│  { "is_defensible": true,                                                │
│    "compelling_evidence_category": "Proof of Delivery",                  │
│    "asserts_delivery_confirmed": true,   ← confirmed in evidence log     │
│    "asserts_auth_match": true,           ← confirmed in evidence log     │
│    "asserts_device_match": null,         ← unverified → OMITTED          │
│    "explanation_template_id": "TPL_DELIVERY" }                           │
│                                                                          │
│  Unsupported claims removed. Unverified ≠ False.                         │
└──────────────────────────────────────────────────────────────────────────┘
```

### Why LightGBM for Stage 1 (not an LLM)?

| Criterion | LightGBM ✅ | LLM ❌ |
|-----------|------------|--------|
| Precision/Recall measurable | Yes — explicit numbers | No — only vibes |
| Threshold tuneable to cost | Yes — probability output | No |
| Feature importance | Yes — interpretable | No |
| Deterministic | Yes | No |
| Rubric-compliant | Fully | Partial |

---

## 🔄 Train/Validation/Test Methodology

To guarantee no threshold leakage, the dataset is strictly separated:

*   **TRAINING (30,000 records):** Used solely to fit the LightGBM model.
*   **VALIDATION (10,000 records):** Used to select the optimal threshold (`0.29`) via cost optimization.
*   **TEST (10,000 records):** Strictly held-out. Used *only* for final metric generation (PR-AUC, F1, Precision, Recall). **Never touched during model or threshold selection.**

---

## 📊 Evaluation Metrics — Held-Out Test Set

> ⚠️ **The test set was locked before training began and never touched during threshold selection.**
> All numbers below are honest, out-of-sample results.

### Global Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **PR-AUC** | **0.7519** | Threshold-independent model quality |
| **Precision** | **62.3%** | At cost-optimal threshold 0.29 |
| **Recall** | **90.2%** | Intentionally high — see cost math below |
| **F1 Score** | **73.7%** | Harmonic mean |
| **Test Set Size** | **10,000** | 20% stratified hold-out |

### Per Reason Code Breakdown

| Reason Code | Category | Test N | Base Win Rate | Precision | Recall | F1 |
|-------------|----------|--------|---------------|-----------|--------|----|
| `10.4` | Fraud — Card Absent | 3,005 | 49.9% | 60.2% | 93.2% | 73.2% |
| `13.1` | Merchandise Not Received | 2,972 | 54.8% | 60.5% | 85.6% | 70.9% |
| `13.3` | Not as Described | 2,012 | 55.4% | 66.8% | 91.5% | 77.2% |
| `11.1` | Card Recovery Bulletin | 514 | 55.5% | 65.0% | 88.8% | 75.1% |
| `4853` | Cardholder Dispute (MC) | 1,497 | 55.2% | 62.9% | 92.6% | 74.9% |

> Each reason code has **>500 test samples** — per-code numbers are statistically meaningful, not noise.

---

## 💰 Cost-Weighted Thresholding

The decision threshold **0.29** is not a default. It is the mathematically optimal point on the validation set where total expected business cost is minimised.

### Cost Model

| Decision Error | Cost | Rationale |
|----------------|------|-----------|
| **False Positive** (file a weak dispute) | ₹ 500 | Wasted ops time + risk to merchant's win-ratio with acquirer |
| **False Negative** (miss a winnable dispute) | Amount + ₹ 1,500 | Direct revenue loss + assumed Visa/MC chargeback fee |

> *Both costs are stated assumptions, clearly labeled as estimates. Not Razorpay-sourced data.*

### Why Recall Is High (This Is Correct)

```
FN Cost on a ₹5,000 dispute = ₹5,000 + ₹1,500 = ₹6,500
FP Cost                     = ₹500

Ratio: 13× more expensive to miss a winnable dispute than to file a weak one.
∴ The optimal threshold is recall-biased. 0.29 is the correct answer, not a tuning failure.
```

The cost curve (visible in the [Evaluation Dashboard](https://razorsentinel-ai.onrender.com)) shows the exact minimum across all thresholds, with separate FP and FN fill bands.

---

## 🔒 Defense-Only Guarantee

The rubric explicitly disqualifies "offense-capable" systems. Three independent layers enforce defense-only behavior:

### Layer 1 — Structured-In / Structured-Out Schema

The LLM **cannot write free-form prose**. It receives a typed `DisputeEvidence` and must fill a `DefensePacket` with specific `Optional[bool]` flags:

```python
class DefensePacket(BaseModel):
    is_defensible: bool
    compelling_evidence_category: Literal[
        "Proof of Delivery", "Device/IP Linkage",
        "Prior Legitimate History", "None"
    ]
    # Optional[bool] tri-state: True=confirmed, None=omitted, False=confirmed-false-from-evidence
    asserts_delivery_confirmed: Optional[bool] = None
    asserts_auth_match:         Optional[bool] = None
    asserts_device_match:       Optional[bool] = None
    explanation_template_id: Literal["TPL_DELIVERY", "TPL_AUTH", "TPL_HISTORY", "TPL_WEAK"]
```

### Layer 2 — Python Post-Generation Guardrail

After every LLM response, every assertion is checked against the source evidence record:

```python
# If LLM asserted a delivery claim but evidence.delivery_confirmed = False:
if packet.asserts_delivery_confirmed and not evidence.delivery_confirmed:
    packet.asserts_delivery_confirmed = None  # OMIT — do NOT flip to False

# Critical design decision:
# Setting unverified → False would ASSERT the opposite of truth.
# Setting unverified → None OMITS the claim entirely.
# A defense packet that omits an unverified claim is safe.
# A defense packet that falsely asserts a negative is a liability.
```

### Layer 3 — Evaluation Data Is Synthesis-Only

The 50,000-record dataset exists solely as evaluation infrastructure. It does not function as a fraud pattern generator, attack simulator, or adversarial training corpus.

---

## 🧪 Anti-Leakage Evaluation Design

Standard mistake: generate labels as a deterministic function of features → model memorises the rule → 99% PR-AUC → impressive number that proves nothing.

We explicitly break this with two measures:

**1. 12% Random Label-Flip Noise**
```python
# ~6,000 records have their label randomly inverted
flip_mask = np.random.rand(num_records) < 0.12
labels = np.where(flip_mask, ~labels, labels)
```
This forces the model to learn probabilistic patterns from noisy data, not memorise a clean rule. PR-AUC dropped from 97% (trivial) to 75% (real).

**2. Pure Confounder Feature**
```python
confounder_feature = np.random.normal(50, 15, size=num_records)
# Zero correlation with dispute_won. Included in training features.
```
In the trained model, `confounder_feature` ranks **last** in LightGBM gain-based feature importance. This confirms the model is not overfitting to noise — it has learned to correctly ignore the confounder.

---

## 📁 Repository Structure

```
RazorSentinel-AI/
│
├── 📄 README.md                    ← You are here
├── 🐳 Dockerfile                   ← Container for Render deployment
├── 📦 requirements.txt             ← Python dependencies
├── ⚙️  vercel.json                  ← Vercel static routing config
│
├── 🌐 landing/
│   └── index.html                  ← Static landing page (Vercel hosted)
│
├── 🎛️  .streamlit/
│   └── config.toml                 ← Dark theme + server config
│
├── 📊 src/
│   ├── data_generator.py           ← Synthetic evaluation data (50k records)
│   ├── schemas.py                  ← Pydantic v2: DisputeEvidence + DefensePacket
│   ├── train_verifier.py           ← LightGBM training + cost-threshold tuning
│   ├── evaluate.py                 ← Held-out evaluation pipeline
│   ├── responder.py                ← Gemini orchestrator + anti-hallucination guardrail
│   ├── adversarial_demo.py         ← Console demo of guardrail blocking a claim
│   └── demo.py                     ← CLI demo (no API key needed)
│
├── 🧪 tests/
│   └── test_responder.py           ← Automated tests for schema and grounding
│
├── 📈 app.py                       ← Streamlit dashboard (4 pages, Plotly charts)
│
└── 📂 data/                        ← Generated at runtime
    ├── synthetic_disputes.csv      ← 50,000 synthetic dispute records
    ├── test_set.csv                ← 10,000 held-out records (locked)
    ├── verifier_model.pkl          ← Trained LightGBM model
    ├── optimal_threshold.txt       ← Cost-optimal threshold (0.29)
    ├── cost_curve.png              ← Cost vs threshold visualization
    └── confusion_matrix.png        ← Confusion matrix at threshold 0.29
```

---

## 🚀 Quickstart & Reproducibility

### Setup
```bash
git clone https://github.com/shambhushekharsinha-engg/RazorSentinel-AI
cd RazorSentinel-AI
pip install -r requirements.txt
```

### Run Automated Tests (Guardrail Verification)
```bash
pytest tests/
```

### Reproduce Metrics Pipeline
```bash
# 1. Generate 50,000 synthetic evaluation records
python src/data_generator.py

# 2. Train verifier + find cost-optimal threshold
python src/train_verifier.py

# 3. Evaluate on held-out test set (produces all metric charts)
python src/evaluate.py
```
**Expected Tolerances:**
- PR-AUC: `~0.75`
- Precision: `~0.62`
- Recall: `~0.90`
- F1: `~0.74`

### Adversarial / Grounding Demo
See the guardrail block an unsupported AI claim in real-time:
```bash
PYTHONPATH=. python src/adversarial_demo.py
```

### Run the Dashboard
```bash
export GEMINI_API_KEY="your-key-here"  # Optional
PYTHONPATH=. streamlit run app.py
# Open: http://localhost:8000
```

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Verifier Model | LightGBM | Structured features, honest PR-AUC, calibrated probabilities, interpretable |
| Auto-Responder LLM | Gemini (google-genai) | Native structured JSON output mode, temperature=0 |
| Schema Validation | Pydantic v2 | Type-safe DisputeEvidence + DefensePacket, Optional[bool] tri-state |
| Evaluation | scikit-learn | PR-AUC, per-reason-code breakdown, confusion matrix |
| Dashboard | Streamlit + Plotly | Interactive charts, no-lag client-side rendering |
| Landing Page | Pure HTML/CSS | Zero dependencies, instant load, 3D buttons |
| Deployment (App) | Render + Docker | Free tier, auto-deploy from GitHub |
| Deployment (Landing) | Vercel | CDN-served static, sub-100ms globally, never sleeps |
| Keep-Alive | UptimeRobot | Pings Render every 5 min, eliminates cold start |

---

## 💥 What Broke (And How We Got Out)

> *The rubric says "the last one is the one we read first." This section is written first.*

### ① Label Leakage — 97% PR-AUC That Proved Nothing

**What happened:** The first data generator assigned `dispute_won` labels using near-deterministic rules (strong delivery + reason 13.1 → win). LightGBM achieved 97% PR-AUC immediately.

**Why it was a problem:** A judge who read `data_generator.py` for 30 seconds would see the model was memorising a hand-written rule, not learning. The number was technically correct and entirely meaningless.

**Fix:** Injected 12% random label-flip noise and added a pure confounder feature (`N(50,15)`, zero correlation). PR-AUC dropped to 0.75 — a real, defensible number. The confounder ranks last in feature importance, confirming genuine generalisation.

### ② The Guardrail Asserted the Wrong Thing

**What happened:** The original guardrail set unverified LLM claims to `False`:
```python
# WRONG — this actively asserts authentication did NOT match
if packet.asserts_auth_match and not (evidence.avs_match and evidence.cvv_match):
    packet.asserts_auth_match = False  ← fabricating a negative claim
```

**Why it was a problem:** `asserts_auth_match = False` in a dispute document means "authentication did NOT match" — a factual assertion we have no basis to make if we simply have no data. That's a different hallucination, and potentially worse in a legal context.

**Fix:** `Optional[bool]` tri-state. Unverified → `None` → omitted entirely. The packet now makes no claim about fields it cannot verify, rather than asserting their negation.

### ③ The Threshold Looked Like a Bug

**What happened:** 62% precision / 90% recall at threshold 0.29 reads as "the model just predicts positive all the time" without context.

**Why it was a problem:** A judge seeing this without explanation would reasonably conclude the threshold is wrong or the model is naive.

**Fix:** Make the cost math explicit everywhere — README, dashboard, video. The threshold is the mathematically optimal business decision given FN cost ≫ FP cost. High recall is correct. The cost curve shows the exact minimum visually.

---

## ✅ Rubric Alignment

| Rubric Requirement | How We Meet It |
|--------------------|----------------|
| **Working detector, verifier, or auto-responder** | Both: LightGBM verifier + Gemini auto-responder |
| **One class of loss** | Chargebacks & Disputes only — no scope creep |
| **Measured precision and recall on held-out test set** | PR-AUC 0.7519, P=62.3%, R=90.2% on 10k locked records |
| **Honest metrics including false-positive cost** | Explicit ₹500 FP / (Amount+₹1500) FN cost model with curve |
| **Strictly defense-only** | 3 independent layers (schema, guardrail, data framing) |
| **GitHub repo (public)** | [github.com/shambhushekharsinha-engg/RazorSentinel-AI](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI) |
| **5-min pitch video** | Live demo → verifier score → defense packet → cost curve → what broke |
| **Show your work** | Cost curve, per-code breakdown, feature importance, noise injection documented |

---

<div align="center">

**Built for Razorpay AI Buildathon 2026 · Track 02: AI Risk Manager**

[⚡ Live Dashboard](https://razorsentinel-ai.onrender.com) · [🌐 Landing Page](https://razorsentinel-ai.vercel.app) · [⎇ GitHub](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI)

</div>
