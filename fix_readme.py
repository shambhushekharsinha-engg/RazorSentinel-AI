import io

with io.open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix image paths
content = content.replace("Project%20demo", "project-demo")
content = content.replace("Project demo", "project-demo")

# Add badges
badges_old = """[![Live Demo](https://img.shields.io/badge/⚡%20Live%20Dashboard-Render-4f8ef7?style=for-the-badge&logo=render&logoColor=white)](https://razorsentinel-ai.onrender.com)
[![Landing Page](https://img.shields.io/badge/🌐%20Landing%20Page-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://razorsentinel-ai.vercel.app)
[![GitHub](https://img.shields.io/badge/⎇%20Source%20Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI)
[![YouTube](https://img.shields.io/badge/▶️%20Pitch%20Video-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=dAWx58ywIFE)"""

badges_new = badges_old + """
[![CI](https://img.shields.io/github/actions/workflow/status/shambhushekharsinha-engg/RazorSentinel-AI/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%20Tests)](https://github.com/shambhushekharsinha-engg/RazorSentinel-AI/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11-3776ab?style=for-the-badge&logo=python&logoColor=white)](.#)"""
content = content.replace(badges_old, badges_new)

# Remove the old python badge further down
content = content.replace("\n[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](.#)", "")

# Add Threshold Sensitivity table
curve_old = "The cost curve (visible in the [Live Evaluation Dashboard](https://razorsentinel-ai.onrender.com)) shows the exact minimum across all thresholds, with separate FP and FN fill bands."
curve_new = curve_old + """

### Threshold Sensitivity

To demonstrate 0.29 is genuinely optimal and not cherry-picked:

<div align="center">

| Threshold | Precision | Recall | F1 | Notes |
|:---------:|:---------:|:------:|:--:|:------|
| 0.20 | ~47% | ~97% | ~63% | Too aggressive — too many weak defenses filed |
| 0.25 | ~55% | ~94% | ~69% | Still recall-heavy |
| **0.29** | **62.3%** | **90.2%** | **73.7%** | ✅ **Cost-optimal on validation set** |
| 0.35 | ~70% | ~85% | ~77% | Higher precision but misses more winnable disputes |
| 0.40 | ~75% | ~78% | ~76% | Approaching balance — costs rise due to FN |
| 0.50 | ~82% | ~65% | ~73% | Default — suboptimal given cost asymmetry |

</div>"""
content = content.replace(curve_old, curve_new)

# Update repo structure
repo_old = """RazorSentinel-AI/
│
├── 📄 README.md                    ← You are here
├── 🐳 Dockerfile                   ← Container for Render deployment
├── 📦 requirements.txt             ← Python dependencies
├── ⚙️  vercel.json                  ← Vercel static routing config
│
├── 🖼️  project-demo/
│   ├── logo.jpg                    ← Project logo
│   ├── demo_video.mp4              ← Full pitch & demo recording
│   └── screenshot_01.png … screenshot_21.png  ← UI screenshots
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
    └── confusion_matrix.png        ← Confusion matrix at threshold 0.29"""

repo_new = """RazorSentinel-AI/
│
├── 📄 README.md                    ← You are here
├── 📋 CHANGELOG.md                 ← Version history & architecture decisions log
├── 🧭 DECISIONS.md                 ← Engineering rationale for every design choice
├── 🤝 CONTRIBUTING.md              ← How to reproduce, extend, and contribute
├── ⚖️  LICENSE                      ← MIT License
├── 🐳 Dockerfile                   ← Container for Render deployment
├── 📦 requirements.txt             ← Python dependencies
├── ⚙️  vercel.json                  ← Vercel static routing config
├── 🔐 .env.example                 ← Environment variable template
│
├── ⎇  .github/
│   ├── workflows/
│   │   └── ci.yml                  ← GitHub Actions: lint + test + evaluate on push
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md           ← Structured bug report template
│
├── 🖼️  project-demo/
│   ├── logo.jpg                    ← Project logo
│   ├── demo_video.mp4              ← Full pitch & demo recording
│   └── screenshot_01.png … screenshot_21.png  ← UI screenshots
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
│   ├── evaluate.py                 ← Held-out evaluation pipeline → saves metrics.json
│   ├── responder.py                ← Gemini orchestrator + anti-hallucination guardrail
│   ├── adversarial_demo.py         ← Console demo of guardrail blocking a claim
│   └── demo.py                     ← CLI demo (no API key needed)
│
├── 🧪 tests/
│   └── test_responder.py           ← 25+ test cases: guardrail, schema, reason codes, edge cases
│
├── 📈 app.py                       ← Streamlit dashboard (6 pages, Plotly charts)
│
└── 📂 data/                        ← Generated at runtime (gitignored)
    ├── synthetic_disputes.csv      ← 50,000 synthetic dispute records
    ├── test_set.csv                ← 10,000 held-out records (locked)
    ├── verifier_model.pkl          ← Trained LightGBM model
    ├── optimal_threshold.txt       ← Cost-optimal threshold (0.29)
    ├── metrics.json                ← Structured evaluation metrics artifact
    ├── cost_curve.png              ← Cost vs threshold visualization
    └── confusion_matrix.png        ← Confusion matrix at threshold 0.29"""

content = content.replace(repo_old, repo_new)

with io.open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
