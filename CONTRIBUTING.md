# Contributing to RazorSentinel-AI

Thank you for your interest in RazorSentinel-AI! This document explains how to reproduce the pipeline, extend the system, and contribute improvements.

---

## 🚀 Quickstart for Contributors

### 1. Fork & Clone

```bash
git clone https://github.com/shambhushekharsinha-engg/RazorSentinel-AI
cd RazorSentinel-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install flake8  # for linting
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 5. Reproduce the Full Pipeline

```bash
# Generate synthetic data
python src/data_generator.py

# Train verifier + find cost-optimal threshold
python src/train_verifier.py

# Evaluate on held-out test set
python src/evaluate.py
```

### 6. Run Tests

```bash
PYTHONPATH=. pytest tests/ -v
```

### 7. Run the Dashboard

```bash
PYTHONPATH=. streamlit run app.py
```

---

## 🏗️ Project Architecture

```
src/
├── data_generator.py   ← Synthetic data with 12% label noise + confounder
├── schemas.py          ← Pydantic models: DisputeEvidence, DefensePacket
├── train_verifier.py   ← LightGBM training + cost-optimal threshold selection
├── evaluate.py         ← Held-out test metrics + saves data/metrics.json
├── responder.py        ← Gemini Stage 2 + anti-hallucination guardrail
├── adversarial_demo.py ← CLI guardrail demo
└── demo.py             ← CLI demo (no API key needed)
```

---

## 🔧 How to Extend

### Adding a New Reason Code

1. Add the code string to `REASON_CODES` in `src/data_generator.py`
2. Add win-score logic for the new code in `generate_data()`
3. Add the display name to `REASON_MAP` in `app.py`
4. Regenerate data and retrain: `python src/data_generator.py && python src/train_verifier.py`

### Adding a New Evidence Field

1. Add the field to `DisputeEvidence` in `src/schemas.py`
2. Add the corresponding guardrail check in `responder.py`
3. Add a corresponding assertion field to `DefensePacket` (use `Optional[bool]`)
4. Update the feature list in `train_verifier.py` and `evaluate.py`
5. Add a test case in `tests/test_responder.py`

### Changing the Cost Model

Edit the `FP_COST` and `fn_cost()` function in both:
- `src/train_verifier.py` (threshold selection on validation set)
- `src/evaluate.py` (cost curve generation on test set)

Both must use identical cost parameters to ensure the reported threshold matches the evaluated curve.

---

## ✅ Code Standards

- **Formatter**: No enforced formatter, but keep lines under 120 characters
- **Linter**: `flake8` — critical errors (E9, F63, F7, F82) must pass
- **Tests**: All new guardrail logic must have a corresponding test in `tests/`
- **Docstrings**: All public functions must have a docstring
- **No secrets in code**: Use `.env` (gitignored) for all API keys

---

## 🔐 Safety Rules (Non-Negotiable)

1. **Defense-only**: This system must never be used to generate fraudulent dispute evidence
2. **No real cardholder data**: All data must be synthetic; never commit real PII
3. **Guardrail integrity**: The `Optional[bool]` tri-state must never be relaxed — unverified claims must remain `None`, never `False`

---

## 📬 Submitting a Pull Request

1. Create a feature branch: `git checkout -b feature/my-improvement`
2. Make your changes and add tests
3. Run the full test suite: `PYTHONPATH=. pytest tests/ -v`
4. Run the linter: `flake8 src/ tests/ --max-line-length=120`
5. Open a PR with a clear description of what changed and why

---

*Built for Razorpay AI Buildathon 2026 · Track 02: AI Risk Manager*
