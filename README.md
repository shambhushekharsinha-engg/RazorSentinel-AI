<div align="center">

<img src="project-demo/logo.jpg" alt="RazorSentinel-AI Logo" width="680" style="border-radius:12px;"/>

<br/><br/>

<img src="https://img.shields.io/badge/ðŸ›¡ï¸%20RazorSentinel--AI-Chargeback%20Defense%20Platform-0d1526?style=for-the-badge&labelColor=050914" alt="RazorSentinel-AI"/>

<br/><br/>

[![Live Demo](https://img.shields.io/badge/âš¡%20Live%20Dashboard-Render-4f8ef7?style=for-the-badge&logo=render&logoColor=white)](https://razorsentinel-ai.onrender.com)
[![Landing Page](https://img.shields.io/badge/ðŸŒ%20Landing%20Page-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://razorsentinel-ai.vercel.app)
[![GitHub](https://img.shields.io/badge/âŽ‡%20Source%20Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI)
[![YouTube](https://img.shields.io/badge/â–¶%20Pitch%20Video-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=dAWx58ywIFE)
[![CI](https://img.shields.io/github/actions/workflow/status/shambhushekharsinha-engg/RazorSentinel-AI/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%20Tests)](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-3776ab?style=for-the-badge&logo=python&logoColor=white)](.#)

<br/>

[![Track](https://img.shields.io/badge/Track%2002-AI%20Risk%20Manager-6366f1?style=for-the-badge)](.#)
[![Defense Only](https://img.shields.io/badge/Architecture-Defense%20Only%20âœ…-10b981?style=for-the-badge)](.#)
[![PR-AUC](https://img.shields.io/badge/PR--AUC-0.7519-f59e0b?style=for-the-badge)](.#)
[![Recall](https://img.shields.io/badge/Recall-90.2%25-22d3ee?style=for-the-badge)](.#)
[![Claims](https://img.shields.io/badge/Claims-Grounded%20âœ“-ef4444?style=for-the-badge)](.#)

<br/><br/>

## ðŸ›¡ï¸ RazorSentinel-AI

### *Autonomous Chargeback Verifier & Evidence Responder*

**Razorpay AI Buildathon 2026 Â· Track 02: AI Risk Manager**

<br/>

> *Stop merchants from losing money to chargebacks â€” with an autonomous two-stage system that verifies disputes and generates evidence-grounded defense packets, mathematically guaranteeing the removal of unsupported claims.*

<br/>

</div>

---

## ðŸ“‹ Table of Contents

<div align="center">

| Section | Description |
|:-------:|:-----------:|
| [ðŸŽ¥ Demo & Gallery](#-video-demo--screenshots) | Pitch video and 21 interface screenshots |
| [ðŸŽ¯ What It Solves](#-what-it-solves) | The chargeback double-loss problem |
| [ðŸ’³ Razorpay Integration](#-razorpay-integration-boundary) | Integration scope and safety boundaries |
| [ðŸ—ï¸ Architecture](#%EF%B8%8F-architecture) | Two-stage pipeline deep dive |
| [ðŸ”„ Methodology](#-trainvalidationtest-methodology) | Train/Validation/Test split strategy |
| [ðŸ“Š Metrics](#-evaluation-metrics--held-out-test-set) | Held-out test set results |
| [ðŸ’° Cost Thresholding](#-cost-weighted-thresholding) | Why recall is intentionally high |
| [ðŸ”’ Defense Guarantee](#-defense-only-guarantee) | Three independent safety layers |
| [ðŸ§ª Anti-Leakage](#-anti-leakage-evaluation-design) | How we prevent evaluation cheating |
| [ðŸ“ Repo Structure](#-repository-structure) | File and folder layout |
| [ðŸš€ Quickstart](#-quickstart--reproducibility) | Get running in minutes |
| [ðŸ› ï¸ Tech Stack](#%EF%B8%8F-tech-stack) | Technologies and rationale |
| [ðŸ’¥ What Broke](#-what-broke-and-how-we-got-out) | Engineering war stories |
| [âœ… Rubric Alignment](#-rubric-alignment) | Buildathon checklist |

</div>

---

## ðŸŽ¥ Video Demo & Screenshots

<div align="center">

**â–¶ Watch the full 5-minute pitch and live demo:**

<a href="https://www.youtube.com/watch?v=dAWx58ywIFE">
  <img src="https://img.youtube.com/vi/dAWx58ywIFE/maxresdefault.jpg" width="800" alt="RazorSentinel-AI â€” 5-Minute Pitch & Live Demo" style="border-radius:8px;"/>
</a>

*Click to watch on YouTube*

</div>

<br/>

### ðŸ“¸ Application Gallery

<details>
<summary><b>ðŸ–¼ï¸ Click to expand â€” 21 interface screenshots</b></summary>

<br/>

<table>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_01.png" alt="Dashboard Overview"/><br/><sub><b>Dashboard Overview</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_02.png" alt="Dispute Verifier"/><br/><sub><b>Dispute Verifier</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_03.png" alt="Evidence Responder"/><br/><sub><b>Evidence Responder</b></sub></td>
  </tr>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_04.png" alt="Defense Packet Output"/><br/><sub><b>Defense Packet Output</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_05.png" alt="PR-AUC Curve"/><br/><sub><b>PR-AUC Curve</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_06.png" alt="Cost Threshold Curve"/><br/><sub><b>Cost Threshold Curve</b></sub></td>
  </tr>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_07.png" alt="Confusion Matrix"/><br/><sub><b>Confusion Matrix</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_08.png" alt="Feature Importance"/><br/><sub><b>Feature Importance</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_09.png" alt="Per Reason Code Metrics"/><br/><sub><b>Per Reason Code Metrics</b></sub></td>
  </tr>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_10.png" alt="Guardrail Demo"/><br/><sub><b>Guardrail Demo</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_11.png" alt="Adversarial Blocking"/><br/><sub><b>Adversarial Blocking</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_12.png" alt="Schema Validation"/><br/><sub><b>Schema Validation</b></sub></td>
  </tr>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_13.png" alt="Evidence Fields"/><br/><sub><b>Evidence Fields</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_14.png" alt="Win Probability Score"/><br/><sub><b>Win Probability Score</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_15.png" alt="Defense Packet JSON"/><br/><sub><b>Defense Packet JSON</b></sub></td>
  </tr>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_16.png" alt="Evaluation Pipeline"/><br/><sub><b>Evaluation Pipeline</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_17.png" alt="Data Distribution"/><br/><sub><b>Data Distribution</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_18.png" alt="Label Noise Analysis"/><br/><sub><b>Label Noise Analysis</b></sub></td>
  </tr>
  <tr>
    <td width="33%"><img src="project-demo/screenshot_19.png" alt="Confounder Analysis"/><br/><sub><b>Confounder Analysis</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_20.png" alt="Deployment Architecture"/><br/><sub><b>Deployment Architecture</b></sub></td>
    <td width="33%"><img src="project-demo/screenshot_21.png" alt="Landing Page"/><br/><sub><b>Landing Page</b></sub></td>
  </tr>
</table>

</details>

---

## ðŸŽ¯ What It Solves

Merchants lose money on chargebacks **twice**:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  LOSS #1  â†’  Dispute filed, transaction reversed    â”‚
â”‚  LOSS #2  â†’  Merchant fails to respond with         â”‚
â”‚              compelling evidence in time             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Single loss class targeted:** Chargebacks & Disputes *(exactly as required by the rubric â€” one class, measured deeply).*

RazorSentinel-AI **eliminates the second loss** by automatically:

| Step | Action |
|------|--------|
| ðŸ” **Verify** | Each incoming dispute â€” is it winnable? |
| ðŸ“ **Respond** | For winnable disputes with a structured, evidence-grounded defense packet |
| ðŸ”’ **Guardrail** | Unsupported evidence assertions are prevented from reaching the final packet |

---

## ðŸ’³ Razorpay Integration Boundary

RazorSentinel is designed around **Razorpay payment and dispute evidence workflows**.

> [!IMPORTANT]
> The ML evaluation dataset is **synthetic** because real chargeback data is unavailable for public training and evaluation. Razorpay-specific transaction identifiers and payment context are represented through the evidence schema.

- âœ… Pipeline built specifically for the **Razorpay ecosystem**
- âœ… No claim that the demo has access to production Razorpay dispute data
- âœ… Strict separation ensures **academic and technical safety**

---

## ðŸ—ï¸ Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         INCOMING DISPUTE                                 â”‚
â”‚        (Reason Code + AVS/CVV + Device Trust + IP/Geo + Delivery)       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                â”‚
                                â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    STAGE 1 â€” LightGBM VERIFIER                           â”‚
â”‚                                                                          â”‚
â”‚  Features: 11 structured evidence fields                                 â”‚
â”‚  â€¢ AVS Match         â€¢ CVV Match          â€¢ Device Trust Score (0â€“1)    â”‚
â”‚  â€¢ IP/Geo Match      â€¢ Delivery Confirmed â€¢ Is Digital Good              â”‚
â”‚  â€¢ Customer History  â€¢ Prior Disputes     â€¢ Transaction Amount           â”‚
â”‚  â€¢ Reason Code       â€¢ Confounder (noise) â† proves model generalises    â”‚
â”‚                                                                          â”‚
â”‚  Output: Win probability P(win | evidence)                               â”‚
â”‚  Threshold: 0.29  (cost-optimal, NOT a default)                          â”‚
â”‚                                                                          â”‚
â”‚  Metric: PR-AUC 0.7519 on 10,000 held-out records                       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                â”‚
                     if P > 0.29 â†’ DEFENSIBLE
                                â”‚
                                â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   STAGE 2 â€” GEMINI AUTO-RESPONDER                        â”‚
â”‚                                                                          â”‚
â”‚  Input:  DisputeEvidence (Pydantic model â€” strictly typed)               â”‚
â”‚  Output: DefensePacket   (Pydantic model â€” Optional[bool] fields)        â”‚
â”‚                                                                          â”‚
â”‚  LLM constraints:                                                        â”‚
â”‚  â€¢ No free-form prose â€” must fill a fixed Boolean field schema           â”‚
â”‚  â€¢ Temperature = 0.0  â€” deterministic output                             â”‚
â”‚  â€¢ response_mime_type = "application/json" â€” structured only             â”‚
â”‚                                                                          â”‚
â”‚  Post-generation Python guardrail:                                       â”‚
â”‚  â€¢ Every LLM assertion checked against source evidence                   â”‚
â”‚  â€¢ Unverified claim â†’ None (omitted), NEVER flipped to False             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                â”‚
                                â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    DEFENSE PACKET JSON OUTPUT                            â”‚
â”‚                                                                          â”‚
â”‚  { "is_defensible": true,                                                â”‚
â”‚    "compelling_evidence_category": "Proof of Delivery",                  â”‚
â”‚    "asserts_delivery_confirmed": true,   â† confirmed in evidence log     â”‚
â”‚    "asserts_auth_match": true,           â† confirmed in evidence log     â”‚
â”‚    "asserts_device_match": null,         â† unverified â†’ OMITTED          â”‚
â”‚    "explanation_template_id": "TPL_DELIVERY" }                           â”‚
â”‚                                                                          â”‚
â”‚  Unsupported claims removed.  Unverified â‰  False.                        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Why LightGBM for Stage 1 â€” Not an LLM?

| Criterion | LightGBM âœ… | LLM âŒ |
|-----------|:----------:|:------:|
| Precision/Recall measurable | âœ… Explicit numbers | âŒ Only vibes |
| Threshold tuneable to cost | âœ… Probability output | âŒ No |
| Feature importance | âœ… Interpretable | âŒ Black box |
| Deterministic | âœ… Yes | âŒ No |
| Rubric-compliant | âœ… Fully | âš ï¸ Partial |

---

## ðŸ”„ Train/Validation/Test Methodology

To guarantee no threshold leakage, the dataset is **strictly separated** across three non-overlapping splits:

```
50,000 Total Records
â”œâ”€â”€ ðŸ‹ï¸  TRAINING    â€” 30,000 records  â†’  Fit the LightGBM model
â”œâ”€â”€ ðŸŽ›ï¸  VALIDATION  â€” 10,000 records  â†’  Select optimal threshold (0.29) via cost optimization
â””â”€â”€ ðŸ”’  TEST        â€” 10,000 records  â†’  Final metric generation ONLY â€” never touched during model or threshold selection
```

> [!IMPORTANT]
> The test set was **locked before training began** and never used during threshold selection. All reported metrics are honest, out-of-sample results.

---

## ðŸ“Š Evaluation Metrics â€” Held-Out Test Set

### Global Metrics

<div align="center">

| Metric | Value | Notes |
|:------:|:-----:|:-----:|
| **PR-AUC** | **0.7519** | Threshold-independent model quality |
| **Precision** | **62.3%** | At cost-optimal threshold 0.29 |
| **Recall** | **90.2%** | Intentionally high â€” see cost math below |
| **F1 Score** | **73.7%** | Harmonic mean |
| **Test Set Size** | **10,000** | 20% stratified hold-out |

</div>

### Per Reason Code Breakdown

| Reason Code | Category | Test N | Base Win Rate | Precision | Recall | F1 |
|:-----------:|:---------|:------:|:-------------:|:---------:|:------:|:--:|
| `10.4` | Fraud â€” Card Absent | 3,005 | 49.9% | 60.2% | 93.2% | 73.2% |
| `13.1` | Merchandise Not Received | 2,972 | 54.8% | 60.5% | 85.6% | 70.9% |
| `13.3` | Not as Described | 2,012 | 55.4% | 66.8% | 91.5% | 77.2% |
| `11.1` | Card Recovery Bulletin | 514 | 55.5% | 65.0% | 88.8% | 75.1% |
| `4853` | Cardholder Dispute (MC) | 1,497 | 55.2% | 62.9% | 92.6% | 74.9% |

> [!NOTE]
> Each reason code has **>500 test samples** â€” per-code numbers are statistically meaningful, not noise.

---

## ðŸ’° Cost-Weighted Thresholding

The decision threshold **0.29** is not a default â€” it is the mathematically optimal point on the validation set where **total expected business cost is minimised**.

### Cost Model

<div align="center">

| Decision Error | Cost | Rationale |
|:-------------:|:----:|:----------|
| **False Positive** *(file a weak dispute)* | â‚¹ 500 | Wasted ops time + risk to merchant win-ratio with acquirer |
| **False Negative** *(miss a winnable dispute)* | Amount + â‚¹ 1,500 | Direct revenue loss + assumed Visa/MC chargeback fee |

</div>

> *Both costs are stated assumptions, clearly labeled as estimates. Not Razorpay-sourced data.*

### Why Recall Is High (This Is Correct)

```
FN Cost on a â‚¹5,000 dispute = â‚¹5,000 + â‚¹1,500 = â‚¹6,500
FP Cost                     = â‚¹500

Ratio: 13Ã— more expensive to miss a winnable dispute than to file a weak one.
âˆ´ The optimal threshold is recall-biased. 0.29 is the correct answer, not a tuning failure.
```

The cost curve (visible in the [Live Evaluation Dashboard](https://razorsentinel-ai.onrender.com)) shows the exact minimum across all thresholds, with separate FP and FN fill bands.

### Threshold Sensitivity

To demonstrate 0.29 is genuinely optimal and not cherry-picked:

<div align="center">

| Threshold | Precision | Recall | F1 | Notes |
|:---------:|:---------:|:------:|:--:|:------|
| 0.20 | ~47% | ~97% | ~63% | Too aggressive â€” too many weak defenses filed |
| 0.25 | ~55% | ~94% | ~69% | Still recall-heavy |
| **0.29** | **62.3%** | **90.2%** | **73.7%** | âœ… **Cost-optimal on validation set** |
| 0.35 | ~70% | ~85% | ~77% | Higher precision but misses more winnable disputes |
| 0.40 | ~75% | ~78% | ~76% | Approaching balance â€” costs rise due to FN |
| 0.50 | ~82% | ~65% | ~73% | Default â€” suboptimal given cost asymmetry |

</div>

---

## ðŸ”’ Defense-Only Guarantee

The rubric explicitly disqualifies "offense-capable" systems. **Three independent layers** enforce defense-only behavior:

### Layer 1 â€” Structured-In / Structured-Out Schema

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

### Layer 2 â€” Python Post-Generation Guardrail

After every LLM response, every assertion is checked against the source evidence record:

```python
# If LLM asserted a delivery claim but evidence.delivery_confirmed = False:
if packet.asserts_delivery_confirmed and not evidence.delivery_confirmed:
    packet.asserts_delivery_confirmed = None  # OMIT â€” do NOT flip to False

# Critical design decision:
# Setting unverified â†’ False would ASSERT the opposite of truth.
# Setting unverified â†’ None OMITS the claim entirely.
# A defense packet that omits an unverified claim is safe.
# A defense packet that falsely asserts a negative is a liability.
```

### Layer 3 â€” Evaluation Data Is Synthesis-Only

The 50,000-record dataset exists solely as **evaluation infrastructure**. It does not function as a fraud pattern generator, attack simulator, or adversarial training corpus.

---

## ðŸ§ª Anti-Leakage Evaluation Design

> [!WARNING]
> Standard mistake: generate labels as a deterministic function of features â†’ model memorises the rule â†’ 99% PR-AUC â†’ impressive number that proves nothing.

We explicitly break this with **two measures**:

#### 1. 12% Random Label-Flip Noise

```python
# ~6,000 records have their label randomly inverted
flip_mask = np.random.rand(num_records) < 0.12
labels = np.where(flip_mask, ~labels, labels)
```

This forces the model to learn probabilistic patterns from noisy data, not memorise a clean rule.

```
PR-AUC without noise injection:  0.97  â† trivial (model memorised the rule)
PR-AUC with noise injection:      0.75  â† real, defensible, honest
```

#### 2. Pure Confounder Feature

```python
confounder_feature = np.random.normal(50, 15, size=num_records)
# Zero correlation with dispute_won. Included in training features.
```

In the trained model, `confounder_feature` ranks **last** in LightGBM gain-based feature importance â€” confirming the model correctly ignores noise and has learned genuine signal.

---

## ðŸ“ Repository Structure

```
RazorSentinel-AI/
â”‚
â”œâ”€â”€ ðŸ“„ README.md                    â† You are here
â”œâ”€â”€ ðŸ“‹ CHANGELOG.md                 â† Version history & architecture decisions log
â”œâ”€â”€ ðŸ§­ DECISIONS.md                 â† Engineering rationale for every design choice
â”œâ”€â”€ ðŸ¤ CONTRIBUTING.md              â† How to reproduce, extend, and contribute
â”œâ”€â”€ âš–ï¸  LICENSE                      â† MIT License
â”œâ”€â”€ ðŸ³ Dockerfile                   â† Container for Render deployment
â”œâ”€â”€ ðŸ“¦ requirements.txt             â† Python dependencies
â”œâ”€â”€ âš™ï¸  vercel.json                  â† Vercel static routing config
â”œâ”€â”€ ðŸ” .env.example                 â† Environment variable template
â”‚
â”œâ”€â”€ âŽ‡  .github/
â”‚   â”œâ”€â”€ workflows/
â”‚   â”‚   â””â”€â”€ ci.yml                  â† GitHub Actions: lint + test + evaluate on push
â”‚   â””â”€â”€ ISSUE_TEMPLATE/
â”‚       â””â”€â”€ bug_report.md           â† Structured bug report template
â”‚
â”œâ”€â”€ ðŸ–¼ï¸  project-demo/
â”‚   â”œâ”€â”€ logo.jpg                    â† Project logo
â”‚   â”œâ”€â”€ demo_video.mp4              â† Full pitch & demo recording
â”‚   â””â”€â”€ screenshot_01.png â€¦ screenshot_21.png  â† UI screenshots
â”‚
â”œâ”€â”€ ðŸŒ landing/
â”‚   â””â”€â”€ index.html                  â† Static landing page (Vercel hosted)
â”‚
â”œâ”€â”€ ðŸŽ›ï¸  .streamlit/
â”‚   â””â”€â”€ config.toml                 â† Dark theme + server config
â”‚
â”œâ”€â”€ ðŸ“Š src/
â”‚   â”œâ”€â”€ data_generator.py           â† Synthetic evaluation data (50k records)
â”‚   â”œâ”€â”€ schemas.py                  â† Pydantic v2: DisputeEvidence + DefensePacket
â”‚   â”œâ”€â”€ train_verifier.py           â† LightGBM training + cost-threshold tuning
â”‚   â”œâ”€â”€ evaluate.py                 â† Held-out evaluation pipeline â†’ saves metrics.json
â”‚   â”œâ”€â”€ responder.py                â† Gemini orchestrator + anti-hallucination guardrail
â”‚   â”œâ”€â”€ adversarial_demo.py         â† Console demo of guardrail blocking a claim
â”‚   â””â”€â”€ demo.py                     â† CLI demo (no API key needed)
â”‚
â”œâ”€â”€ ðŸ§ª tests/
â”‚   â””â”€â”€ test_responder.py           â† 25+ test cases: guardrail, schema, reason codes, edge cases
â”‚
â”œâ”€â”€ ðŸ“ˆ app.py                       â† Streamlit dashboard (6 pages, Plotly charts)
â”‚
â””â”€â”€ ðŸ“‚ data/                        â† Generated at runtime (gitignored)
    â”œâ”€â”€ synthetic_disputes.csv      â† 50,000 synthetic dispute records
    â”œâ”€â”€ test_set.csv                â† 10,000 held-out records (locked)
    â”œâ”€â”€ verifier_model.pkl          â† Trained LightGBM model
    â”œâ”€â”€ optimal_threshold.txt       â† Cost-optimal threshold (0.29)
    â”œâ”€â”€ metrics.json                â† Structured evaluation metrics artifact
    â”œâ”€â”€ cost_curve.png              â† Cost vs threshold visualization
    â””â”€â”€ confusion_matrix.png        â† Confusion matrix at threshold 0.29
```

---

## ðŸš€ Quickstart & Reproducibility

### 1. Clone & Install

```bash
git clone https://github.com/shambhushekharsinha-engg/RazorSentinel-AI
cd RazorSentinel-AI
pip install -r requirements.txt
```

### 2. Run Automated Tests

Verify the guardrail is working correctly:

```bash
pytest tests/
```

### 3. Reproduce the Full Metrics Pipeline

```bash
# Step 1 â€” Generate 50,000 synthetic evaluation records
python src/data_generator.py

# Step 2 â€” Train verifier + find cost-optimal threshold
python src/train_verifier.py

# Step 3 â€” Evaluate on held-out test set (produces all metric charts)
python src/evaluate.py
```

**Expected tolerances after reproduction:**

| Metric | Expected |
|--------|:--------:|
| PR-AUC | `~0.75` |
| Precision | `~0.62` |
| Recall | `~0.90` |
| F1 | `~0.74` |

### 4. Adversarial / Grounding Demo

See the guardrail **block an unsupported AI claim** in real-time:

```bash
PYTHONPATH=. python src/adversarial_demo.py
```

### 5. Launch the Dashboard

```bash
export GEMINI_API_KEY="your-key-here"   # Optional â€” enables Stage 2 live inference
PYTHONPATH=. streamlit run app.py
# Open: http://localhost:8000
```

> [!TIP]
> No API key? The dashboard still runs fully â€” Stage 1 verifier, all metrics, and cost curves are API-key-free.

---

## ðŸ› ï¸ Tech Stack

<div align="center">

| Component | Technology | Why |
|:----------|:----------:|:----|
| **Verifier Model** | `LightGBM` | Structured features, honest PR-AUC, calibrated probabilities, interpretable |
| **Auto-Responder LLM** | `Gemini (google-genai)` | Native structured JSON output mode, temperature=0 determinism |
| **Schema Validation** | `Pydantic v2` | Type-safe DisputeEvidence + DefensePacket, Optional[bool] tri-state |
| **Evaluation** | `scikit-learn` | PR-AUC, per-reason-code breakdown, confusion matrix |
| **Dashboard** | `Streamlit + Plotly` | Interactive charts, no-lag client-side rendering |
| **Landing Page** | `Pure HTML/CSS` | Zero dependencies, instant load, 3D buttons |
| **Deployment (App)** | `Render + Docker` | Free tier, auto-deploy from GitHub |
| **Deployment (Landing)** | `Vercel` | CDN-served static, sub-100ms globally, never sleeps |
| **Keep-Alive** | `UptimeRobot` | Pings Render every 5 min, eliminates cold starts |

</div>

---

## ðŸ’¥ What Broke (And How We Got Out)

> *The rubric says "the last one is the one we read first." This section is written first.*

### â‘  Label Leakage â€” 97% PR-AUC That Proved Nothing

**What happened:** The first data generator assigned `dispute_won` labels using near-deterministic rules (strong delivery + reason 13.1 â†’ win). LightGBM achieved 97% PR-AUC immediately.

**Why it was a problem:** A judge who read `data_generator.py` for 30 seconds would see the model was memorising a hand-written rule, not learning. The number was technically correct and entirely meaningless.

**The fix:**

```python
# Injected 12% random label-flip noise
flip_mask = np.random.rand(num_records) < 0.12
labels = np.where(flip_mask, ~labels, labels)
# PR-AUC dropped from 0.97 â†’ 0.75 â€” a real, defensible number
```

The confounder ranks last in feature importance, confirming genuine generalisation.

---

### â‘¡ The Guardrail Asserted the Wrong Thing

**What happened:** The original guardrail set unverified LLM claims to `False`:

```python
# WRONG â€” this actively asserts authentication did NOT match
if packet.asserts_auth_match and not (evidence.avs_match and evidence.cvv_match):
    packet.asserts_auth_match = False  # â† fabricating a negative claim
```

**Why it was a problem:** `asserts_auth_match = False` in a dispute document means "authentication did NOT match" â€” a factual assertion we have no basis to make. That is a different hallucination, potentially worse in a legal context.

**The fix:** `Optional[bool]` tri-state. Unverified â†’ `None` â†’ **omitted entirely**. The packet now makes no claim about fields it cannot verify, rather than asserting their negation.

---

### â‘¢ The Threshold Looked Like a Bug

**What happened:** 62% precision / 90% recall at threshold 0.29 reads as "the model just predicts positive all the time" without context.

**Why it was a problem:** A judge seeing this without explanation would reasonably conclude the threshold is wrong or the model is naive.

**The fix:** Make the cost math explicit everywhere â€” README, dashboard, video. The threshold is the mathematically optimal business decision given FN cost â‰« FP cost. High recall is correct. The cost curve shows the exact minimum visually.

---

## âœ… Rubric Alignment

<div align="center">

| Rubric Requirement | Status | How We Meet It |
|:------------------|:------:|:--------------|
| **Working detector, verifier, or auto-responder** | âœ… | Both: LightGBM verifier + Gemini auto-responder |
| **One class of loss** | âœ… | Chargebacks & Disputes only â€” no scope creep |
| **Measured precision and recall on held-out test set** | âœ… | PR-AUC 0.7519, P=62.3%, R=90.2% on 10k locked records |
| **Honest metrics including false-positive cost** | âœ… | Explicit â‚¹500 FP / (Amount+â‚¹1500) FN cost model with curve |
| **Strictly defense-only** | âœ… | 3 independent layers (schema, guardrail, data framing) |
| **GitHub repo (public)** | âœ… | [github.com/shambhushekharsinha-engg/RazorSentinel-AI](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI) |
| **5-min pitch video** | âœ… | Live demo â†’ verifier score â†’ defense packet â†’ cost curve â†’ what broke |
| **Show your work** | âœ… | Cost curve, per-code breakdown, feature importance, noise injection documented |

</div>

---

<div align="center">

<br/>

**Built with â¤ï¸ for Razorpay AI Buildathon 2026 Â· Track 02: AI Risk Manager**

<br/>

[![Live Dashboard](https://img.shields.io/badge/âš¡%20Live%20Dashboard-4f8ef7?style=for-the-badge&logo=render&logoColor=white)](https://razorsentinel-ai.onrender.com)
[![Landing Page](https://img.shields.io/badge/ðŸŒ%20Landing%20Page-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://razorsentinel-ai.vercel.app)
[![Source Code](https://img.shields.io/badge/âŽ‡%20Source%20Code-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI)
[![Pitch Video](https://img.shields.io/badge/â–¶%20Pitch%20Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=dAWx58ywIFE)

<br/><br/>

*Â© 2026 Shambhu Shekhar Sinha Â· RazorSentinel-AI*

</div>
