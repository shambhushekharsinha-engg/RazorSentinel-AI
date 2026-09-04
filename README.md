# 🛡️ RazorSentinel-AI

**Razorpay AI Buildathon · Track 02: AI Risk Manager**

> *Stop the merchant losing money to chargebacks — with an autonomous verifier that only makes claims it can prove.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-blue?style=for-the-badge)](https://razorsentinel-ai.onrender.com)
[![Track](https://img.shields.io/badge/Track-02%20AI%20Risk%20Manager-1a56ff?style=for-the-badge)]()
[![Defense Only](https://img.shields.io/badge/Defense-Only%20%E2%9C%85-00d26a?style=for-the-badge)]()
[![PR-AUC](https://img.shields.io/badge/PR--AUC-0.7519-orange?style=for-the-badge)]()

---

## What it solves

Merchants lose money on chargebacks **twice**: when the dispute is filed, and again when they fail to file a compelling evidence response in time. RazorSentinel-AI eliminates the second loss by:

1. **Verifying** each incoming dispute (is it winnable?)
2. **Auto-responding** for winnable disputes with a zero-hallucination, evidence-grounded defense packet

**Single loss class:** Chargebacks & Disputes — exactly as the rubric requires.

---

## Architecture

```
Incoming Dispute
       │
       ▼
┌──────────────────────────────────────┐
│  STAGE 1 · LightGBM Verifier         │
│  11 structured evidence features     │
│  → Win probability score (0–1)       │
│  → Cost-optimal threshold: 0.29      │
└──────────────┬───────────────────────┘
               │  if prob > 0.29
               ▼
┌──────────────────────────────────────┐
│  STAGE 2 · Gemini Auto-Responder     │
│  Structured-in / structured-out      │
│  Pydantic schema (no free-form text) │
│  → Python guardrail: drops any LLM   │
│     claim not confirmed in evidence  │
│  → Output: Optional[bool] fields     │
│     (unverified → None, not False)   │
└──────────────────────────────────────┘
               │
               ▼
        Defense Packet JSON
        (zero hallucination guaranteed)
```

**Why LightGBM, not an LLM, for Stage 1?** Real-time triage needs deterministic, interpretable scores. LightGBM gives feature importance, honest precision/recall, and a calibrated probability — not a persuasive sentence. The LLM is confined to Stage 2 where it is strictly constrained by schema.

---

## Honest Metrics (Held-Out Test Set · 10,000 records)

> These numbers were produced on a test split **never touched** during training or threshold selection.

| Metric | Value |
|--------|-------|
| **PR-AUC** (threshold-independent) | **0.7519** |
| Precision @ threshold 0.29 | 62.3% |
| Recall @ threshold 0.29 | 90.2% |
| F1 Score | 73.7% |
| Test Set Size | 10,000 |

### Why is Recall so high and Precision lower?

This is **intentional and mathematically correct**, not a tuning failure. The cost model:

| Decision Error | Cost |
|----------------|------|
| **False Positive** — file a weak dispute that loses | ₹500 *(ops time + acquirer win-ratio penalty)* |
| **False Negative** — miss a winnable dispute | Amount + ₹1,500 *(direct loss + assumed Visa/MC fee)* |

> *Cost assumptions are stated estimates, not Razorpay-sourced data.*

At threshold 0.29, total expected cost on the test set is mathematically minimised. Missing a winnable ₹5,000 dispute costs ₹6,500; filing a weak one costs ₹500. The math forces a recall-biased threshold.

### Per Reason Code Breakdown

| Reason Code | Description | N | Precision | Recall |
|-------------|-------------|---|-----------|--------|
| 10.4 | Fraud — Card Absent | 3,005 | 60.2% | 93.2% |
| 13.1 | Merchandise Not Received | 2,972 | 60.5% | 85.6% |
| 13.3 | Not as Described | 2,012 | 66.8% | 91.5% |
| 11.1 | Card Recovery Bulletin | 514 | 65.0% | 88.8% |
| 4853 | Cardholder Dispute (MC) | 1,497 | 62.9% | 92.6% |

---

## Defense-Only Guarantee

The rubric explicitly requires defense-only architecture. Three layers enforce this:

### 1. Structured-in / Structured-out Schema
The LLM cannot write free-form prose. It receives a `DisputeEvidence` Pydantic object and must populate a `DefensePacket` with specific `Optional[bool]` flags:

```python
class DefensePacket(BaseModel):
    is_defensible: bool
    compelling_evidence_category: Literal["Proof of Delivery", "Device/IP Linkage", ...]
    asserts_delivery_confirmed: Optional[bool] = None  # None = omitted, not asserted false
    asserts_device_match: Optional[bool] = None
    asserts_auth_match: Optional[bool] = None
    explanation_template_id: Literal["TPL_DELIVERY", "TPL_AUTH", "TPL_HISTORY", "TPL_WEAK"]
```

### 2. Python Post-Generation Guardrail
After the LLM responds, every assertion is checked against the source evidence:

```python
if packet.asserts_delivery_confirmed and not evidence.delivery_confirmed:
    packet.asserts_delivery_confirmed = None  # Omit — do NOT flip to False
```

**Critical design choice:** Setting an unverified claim to `False` would be *asserting the opposite of truth* — equally wrong. Setting it to `None` omits it from the packet entirely. A dispute document that omits an unverified claim is defensible; one that falsely asserts a negative is not.

### 3. Evaluation Data Is Synthesis-Only
The synthetic dataset is evaluation infrastructure. It is documented explicitly as such and does not function as a fraud pattern generator.

---

## Evaluation Design (Anti-Leakage)

The `dispute_won` label was **not** a clean deterministic function of the training features. Two explicit measures prevent trivial 99% accuracy:

1. **12% random label-flip noise** — ~6,000 records have their label randomly inverted, forcing the model to learn probabilistic patterns, not memorised rules.
2. **Pure confounder feature** — `confounder_feature` is drawn from `N(50, 15)` with zero correlation to the outcome. If the model overfit to noise, this feature would gain importance. It ranks last in LightGBM gain-based importance, confirming genuine generalisation.

The 0.75 PR-AUC on a noisy, confounded test set is a meaningful result, not a demo artifact.

---

## Repository Structure

```
RazorSentinel-AI/
├── app.py                  # Streamlit dashboard (3 pages)
├── Dockerfile              # For Render / container deployment
├── requirements.txt
├── .streamlit/config.toml  # Dark theme + server config
├── src/
│   ├── data_generator.py   # Synthetic evaluation data (50k records)
│   ├── schemas.py          # Pydantic v2 schemas (DisputeEvidence, DefensePacket)
│   ├── train_verifier.py   # LightGBM training + cost-threshold tuning
│   ├── evaluate.py         # Held-out evaluation (PR-AUC, cost curve, confusion matrix)
│   ├── responder.py        # Gemini orchestrator + anti-hallucination guardrail
│   └── demo.py             # CLI demo script
└── data/
    ├── synthetic_disputes.csv
    ├── test_set.csv         # Strictly held-out, never touched during training
    ├── verifier_model.pkl
    ├── optimal_threshold.txt
    ├── cost_curve.png
    └── confusion_matrix.png
```

---

## Quickstart

```bash
git clone https://github.com/shambhushekharsinha-engg/RazorSentinel-AI
cd RazorSentinel-AI
pip install -r requirements.txt

# Generate data, train, evaluate
python src/data_generator.py
python src/train_verifier.py
python src/evaluate.py

# Run dashboard
streamlit run app.py

# Run CLI demo (no GEMINI_API_KEY → deterministic fallback)
PYTHONPATH=. python src/demo.py
```

**With Gemini Auto-Responder:** Set `GEMINI_API_KEY` in your environment. The responder falls back to a deterministic rule-based packet generator if the key is absent — the guardrail runs in both paths.

---

## What Broke (And How We Got Out)

**1. Label leakage killed the first model.** The initial generator used near-deterministic rules for `dispute_won`. LightGBM hit 97% PR-AUC immediately — a number that would have fooled a casual look but collapsed under the question *"is your label a function of your features?"* Fix: 12% label-flip noise + confounder feature. PR-AUC dropped to 0.75 — a real, defensible number.

**2. The guardrail was logically broken.** The first version set unverified LLM claims to `False`. But `asserts_auth_match = False` in a dispute packet means "authentication did NOT match" — a factual assertion we cannot make if we simply have no data. That's a different kind of hallucination. Fix: `Optional[bool]` tri-state. Unverified → `None` → omitted entirely.

**3. The threshold looked like a tuning failure.** 62% precision / 90% recall reads as "the model just predicts positive a lot" without context. Fix: make the cost math explicit in the README, the dashboard, and the video. The threshold is a business decision, not a model deficiency.

---

*Built for Razorpay AI Buildathon 2026 · Track 02: AI Risk Manager*
