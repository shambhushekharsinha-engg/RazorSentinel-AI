# Changelog — RazorSentinel-AI

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-09-05 · Buildathon Submission

### Added
- **Stage 1 — LightGBM Verifier**: Trained on 30,000 synthetic records with 11 structured evidence features. Cost-optimal threshold 0.29 selected on a separate 10,000-record validation set.
- **Stage 2 — Gemini Auto-Responder**: Structured JSON-only output via `response_mime_type="application/json"` and `temperature=0.0`. Accepts `DisputeEvidence`, emits `DefensePacket`.
- **Anti-Hallucination Guardrail**: Post-generation Python check — every LLM `True` assertion is verified against source evidence. Unverified claims set to `None` (omitted), never `False`.
- **`Optional[bool]` Tri-State Schema**: Pydantic v2 `DefensePacket` with `Optional[bool]` fields. Prevents the LLM from asserting the negation of an unverifiable claim.
- **12% Label-Flip Noise**: Injected in `data_generator.py` to prevent trivial rule-memorisation. PR-AUC dropped from 0.97 → 0.75 (a real, defensible number).
- **Pure Confounder Feature**: `confounder_feature ~ N(50, 15)`, zero label correlation, included in training. Ranks last in gain-based feature importance — confirms genuine generalisation.
- **Cost-Weighted Threshold Selection**: FP cost ₹500, FN cost = amount + ₹1500. Threshold 0.29 is the mathematically optimal point on the validation cost curve.
- **Streamlit Dashboard** (6 pages): Overview, Live Triage, Batch Simulator, Guardrail Demo, Evaluation Deep-Dive, About.
- **Batch Queue Simulator**: Score and triage N disputes simultaneously with estimated revenue protection.
- **Adversarial Demo Page**: Interactive UI to configure adversarial evidence and watch the guardrail block unsupported claims in real-time.
- **Evaluation Deep-Dive**: PR curve, cost optimisation curve, confusion matrix, feature importance, per-reason-code breakdown — all computed on held-out test set.
- **Static Landing Page**: Pure HTML/CSS hosted on Vercel (`razorsentinel-ai.vercel.app`).
- **Docker Deployment**: Single-stage Dockerfile builds data + trains model + serves Streamlit on Render.
- **UptimeRobot Keep-Alive**: Eliminates Render cold-start delays.

### Fixed
- **Label Leakage**: Original deterministic label generator gave 97% PR-AUC. Fixed by injecting 12% random label-flip noise and a confounder feature.
- **Guardrail Direction Bug**: Original guardrail set unverified claims to `False` (asserting the negative). Fixed to `None` (omit entirely). A packet asserting delivery=False when we have no data is a fabricated claim.
- **Threshold Presentation**: 0.29 threshold with 62%/90% precision/recall looked like a bug without context. Fixed by making cost math explicit in README, dashboard, and pitch video.

### Architecture Decisions
- **LightGBM over LLM for Stage 1**: Structured features, calibrated probabilities, explicit PR-AUC, tuneable threshold, interpretable feature importance. LLMs have none of these properties.
- **Strict 60/20/20 split**: Test set locked before training begins. Threshold selected only on validation set. Zero data leakage between any two splits.
- **Defense-only by design**: Three independent enforcement layers — Pydantic schema (no free-form prose), Python guardrail (unverified → None), synthesis-only data (no attack patterns).

---

## [0.2.0] — Development Iteration

### Changed
- Replaced `False`-assignment guardrail with `None`-assignment (tri-state fix)
- Replaced deterministic labels with noise-injected labels
- Added confounder feature to training set

---

## [0.1.0] — Initial Prototype

### Added
- Basic LightGBM classifier with default threshold 0.5
- Gemini free-form prose responder (pre-schema enforcement)
- Initial Streamlit single-page dashboard
