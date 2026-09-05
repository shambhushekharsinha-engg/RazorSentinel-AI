<div align="center">

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

## 📋 Table of Contents

- [What It Solves](#-what-it-solves)
- [Razorpay Integration Boundary](#-razorpay-integration-boundary)
- [Architecture](#-architecture)
- [Train/Validation/Test Methodology](#-trainvalidationtest-methodology)
- [Evaluation Metrics](#-evaluation-metrics--held-out-test-set)
- [Cost-Weighted Thresholding](#-cost-weighted-thresholding)
- [Defense-Only Guarantee](#-defense-only-guarantee)
- [Anti-Leakage Design](#-anti-leakage-evaluation-design)
- [Quickstart & Reproducibility](#-quickstart--reproducibility)

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

---

## 🔄 Train/Validation/Test Methodology

To guarantee no threshold leakage, the dataset is strictly separated:

*   **TRAINING (30,000 records):** Used solely to fit the LightGBM model.
*   **VALIDATION (10,000 records):** Used to select the optimal threshold (`0.29`) via cost optimization.
*   **TEST (10,000 records):** Strictly held-out. Used *only* for final metric generation (PR-AUC, F1, Precision, Recall). **Never touched during model or threshold selection.**

---

## 📊 Evaluation Metrics — Held-Out Test Set

> ⚠️ **The test set was locked before training began and never touched during threshold selection.**

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

---

## 💰 Cost-Weighted Thresholding

The decision threshold **0.29** is not a default. It is the mathematically optimal point on the validation set where total expected business cost is minimised.

### Cost Model

| Decision Error | Cost | Rationale |
|----------------|------|-----------|
| **False Positive** (file a weak dispute) | ₹ 500 | Wasted ops time + risk to merchant's win-ratio with acquirer |
| **False Negative** (miss a winnable dispute) | Amount + ₹ 1,500 | Direct revenue loss + assumed Visa/MC chargeback fee |

> *Both costs are stated assumptions, clearly labeled as estimates. Not Razorpay-sourced data.*

---

## 🔒 Defense-Only Guarantee

The rubric explicitly disqualifies "offense-capable" systems. Three independent layers enforce defense-only behavior:

### Layer 1 — Structured-In / Structured-Out Schema

The LLM **cannot write free-form prose**. It receives a typed `DisputeEvidence` and must fill a `DefensePacket` with specific `Optional[bool]` flags.

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
```

### Layer 3 — Evaluation Data Is Synthesis-Only

The dataset exists solely as evaluation infrastructure. It does not function as a fraud pattern generator or attack simulator.

---

## 🧪 Anti-Leakage Evaluation Design

We prevent trivial memorization with two measures:

**1. 12% Random Label-Flip Noise**
This forces the model to learn probabilistic patterns from noisy data, not memorise a clean rule. PR-AUC dropped from 97% (trivial) to 75% (real).

**2. Pure Confounder Feature**
Included `confounder_feature` (`N(50,15)`, zero correlation). In the trained model, it ranks **last** in feature importance, confirming genuine generalisation.

---

## 🚀 Quickstart & Reproducibility

### Setup
```bash
git clone https://github.com/shambhushekharsinha-engg/RazorSentinel-AI
cd RazorSentinel-AI
pip install -r requirements.txt
```

### Run Tests (Guardrail Verification)
```bash
pytest tests/
```

### Reproduce Metrics Pipeline
```bash
# Generate data, train verifier, and evaluate test set
python src/data_generator.py
python src/train_verifier.py
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
python src/adversarial_demo.py
```

### Run the Dashboard
```bash
export GEMINI_API_KEY="your-key-here"  # Optional
PYTHONPATH=. streamlit run app.py
```

---

<div align="center">

**Built for Razorpay AI Buildathon 2026 · Track 02: AI Risk Manager**

[⚡ Live Dashboard](https://razorsentinel-ai.onrender.com) · [🌐 Landing Page](https://razorsentinel-ai.vercel.app) · [⎇ GitHub](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI)

</div>
