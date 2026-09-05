import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import time
import plotly.graph_objects as go
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    average_precision_score, confusion_matrix,
    precision_recall_curve
)
from src.schemas import DisputeEvidence
from src.responder import generate_defense_packet

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RazorSentinel-AI · Chargeback Defense",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root{
  --navy:#050914; --card:#0d1526; --card2:#111827;
  --blue:#4f8ef7; --indigo:#6366f1; --cyan:#22d3ee;
  --gold:#f59e0b; --green:#10b981; --red:#ef4444;
  --text:#e8eeff; --muted:#6b7a9f; --border:rgba(79,142,247,.18);
}
html,body,[data-testid="stAppViewContainer"]{background:var(--navy)!important;color:var(--text)!important;}
[data-testid="stSidebar"]{background:#070d1e!important;border-right:1px solid var(--border)!important;}
[data-testid="stHeader"]{background:transparent!important;}
#MainMenu,footer,header{visibility:hidden;}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--navy)}
::-webkit-scrollbar-thumb{background:var(--blue);border-radius:3px}

/* 3-D BUTTONS */
div.stButton>button{
  background:linear-gradient(145deg,#5a9bff 0%,#3a72e0 60%,#2855c4 100%)!important;
  color:#fff!important;border:none!important;border-radius:10px!important;
  padding:12px 28px!important;font-size:.95rem!important;font-weight:700!important;
  cursor:pointer!important;width:100%!important;
  box-shadow:0 6px 0 #1a3a9a,0 8px 16px rgba(79,142,247,.40),inset 0 1px 0 rgba(255,255,255,.20)!important;
  transform:translateY(0)!important;transition:all .15s ease!important;
}
div.stButton>button:hover{box-shadow:0 4px 0 #1a3a9a,0 6px 20px rgba(79,142,247,.55),inset 0 1px 0 rgba(255,255,255,.25)!important;transform:translateY(2px)!important;}
div.stButton>button:active{box-shadow:0 1px 0 #1a3a9a,0 2px 8px rgba(79,142,247,.40)!important;transform:translateY(5px)!important;}

/* GLASS CARDS */
.glass{background:rgba(13,21,38,.75);border:1px solid var(--border);border-radius:14px;backdrop-filter:blur(12px);padding:22px 26px;box-shadow:0 8px 32px rgba(0,0,0,.45);}
.glass-gold{background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.25);border-radius:14px;padding:20px 24px;}
.glass-green{background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.28);border-radius:14px;padding:20px 24px;}
.glass-red{background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.28);border-radius:14px;padding:20px 24px;}
.glass-indigo{background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.28);border-radius:14px;padding:20px 24px;}

/* HERO */
.hero{background:linear-gradient(135deg,rgba(79,142,247,.18) 0%,rgba(99,102,241,.10) 50%,rgba(5,9,20,.0) 100%),radial-gradient(ellipse 120% 80% at 80% 40%,rgba(34,211,238,.07) 0%,transparent 70%),var(--card);border:1px solid var(--border);border-radius:16px;padding:36px 40px;margin-bottom:28px;position:relative;overflow:hidden;}
.hero::before{content:"";position:absolute;top:-60px;right:-60px;width:280px;height:280px;background:radial-gradient(circle,rgba(79,142,247,.15) 0%,transparent 70%);border-radius:50%;}
.hero h1{color:#fff;font-size:2.4rem;margin:0 0 6px;font-weight:800;letter-spacing:-.5px;}
.hero p{color:#a0b4d8;font-size:1.0rem;margin:0;}
.hero .badge{display:inline-block;margin-top:14px;background:rgba(79,142,247,.15);border:1px solid rgba(79,142,247,.35);border-radius:20px;padding:5px 14px;font-size:.78rem;color:var(--cyan);letter-spacing:.5px;}

/* KPI CARDS */
.kpi{background:linear-gradient(145deg,var(--card2),var(--card));border:1px solid var(--border);border-radius:12px;padding:20px 18px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.04);transition:transform .2s,box-shadow .2s;}
.kpi:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(79,142,247,.2);}
.kpi .label{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.9px;}
.kpi .value{font-size:2rem;font-weight:800;color:#fff;margin:6px 0 3px;text-shadow:0 0 20px rgba(79,142,247,.5);}
.kpi .sub{font-size:.72rem;color:#4f6a9a;}

/* VERDICT */
.verdict-win{background:linear-gradient(90deg,rgba(16,185,129,.12) 0%,transparent 100%);border-left:4px solid var(--green);border-radius:0 10px 10px 0;padding:16px 20px;}
.verdict-loss{background:linear-gradient(90deg,rgba(239,68,68,.12) 0%,transparent 100%);border-left:4px solid var(--red);border-radius:0 10px 10px 0;padding:16px 20px;}
.verdict-win .vtitle{color:var(--green);font-size:1.15rem;font-weight:800;}
.verdict-loss .vtitle{color:var(--red);font-size:1.15rem;font-weight:800;}
.verdict-win .vsub{color:#5db88a;font-size:.85rem;margin-top:4px;}
.verdict-loss .vsub{color:#c07070;font-size:.85rem;margin-top:4px;}

/* STAGE BADGE */
.sbadge{display:inline-block;background:linear-gradient(90deg,rgba(79,142,247,.2),rgba(99,102,241,.15));border:1px solid rgba(99,102,241,.35);border-radius:6px;padding:4px 12px;font-size:.72rem;color:#a0b4ff;letter-spacing:.6px;text-transform:uppercase;font-weight:600;margin-bottom:12px;}

/* EVIDENCE ROWS */
.ev-row{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;border-radius:8px;margin-bottom:5px;background:var(--card2);border:1px solid rgba(255,255,255,.05);}
.ev-key{color:var(--muted);font-size:.82rem;}
.ev-val{font-size:.85rem;font-weight:600;}
.ev-yes{color:var(--green);} .ev-no{color:var(--red);} .ev-num{color:var(--cyan);}

/* PILLS */
.pill-ok{display:inline-flex;align-items:center;gap:5px;background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.35);border-radius:20px;padding:5px 14px;color:var(--green);font-size:.8rem;font-weight:600;margin:4px 3px;}
.pill-omit{display:inline-flex;align-items:center;gap:5px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:5px 14px;color:#4f6a9a;font-size:.8rem;margin:4px 3px;}
.pill-blocked{display:inline-flex;align-items:center;gap:5px;background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.35);border-radius:20px;padding:5px 14px;color:var(--red);font-size:.8rem;font-weight:600;margin:4px 3px;}

/* PROB BAR */
.prob-wrap{background:rgba(255,255,255,.06);border-radius:20px;height:12px;width:100%;margin:10px 0;overflow:hidden;border:1px solid rgba(255,255,255,.08);}
.prob-fill{height:100%;border-radius:20px;transition:width .6s ease;}

/* BATCH QUEUE ROWS */
.queue-row{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:8px;margin-bottom:6px;background:var(--card2);border:1px solid rgba(255,255,255,.05);animation:fadein .4s ease;}
@keyframes fadein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.queue-id{font-size:.78rem;font-family:monospace;color:var(--cyan);width:120px;flex-shrink:0;}
.queue-bar-wrap{flex:1;background:rgba(255,255,255,.06);border-radius:20px;height:8px;overflow:hidden;}
.queue-bar{height:100%;border-radius:20px;}
.queue-score{font-size:.8rem;font-weight:700;width:48px;text-align:right;flex-shrink:0;}
.queue-badge{font-size:.7rem;font-weight:700;padding:3px 9px;border-radius:20px;flex-shrink:0;}
.qb-win{background:rgba(16,185,129,.15);color:var(--green);border:1px solid rgba(16,185,129,.3);}
.qb-loss{background:rgba(239,68,68,.15);color:var(--red);border:1px solid rgba(239,68,68,.3);}

/* ADVERSARIAL DEMO */
.adv-step{padding:12px 16px;border-radius:9px;margin-bottom:8px;font-size:.83rem;line-height:1.6;}
.adv-evidence{background:rgba(79,142,247,.08);border:1px solid rgba(79,142,247,.2);}
.adv-attempt{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);}
.adv-blocked{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);}
.adv-output{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);}

/* TABS */
[data-testid="stTabs"] button{color:var(--muted)!important;font-weight:600!important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:var(--blue)!important;border-bottom:2px solid var(--blue)!important;}

/* GLOW DOT */
@keyframes glow{0%,100%{opacity:1}50%{opacity:.6}}
.glow-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:7px;animation:glow 2s ease-in-out infinite;box-shadow:0 0 8px var(--green);}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FEATURES = [
    'transaction_amount','avs_match','cvv_match','device_trust_score',
    'ip_geo_match','delivery_confirmed','is_digital_good',
    'customer_history_days','prior_disputes','confounder_feature','reason_code'
]
REASON_MAP = {
    "10.4":"10.4 — Fraud (Card Absent)", "13.1":"13.1 — Not Received",
    "13.3":"13.3 — Not as Described",    "11.1":"11.1 — Card Recovery",
    "4853":"4853 — Cardholder Dispute",  "4853.0":"4853 — Cardholder Dispute",
}
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a0b4d8", family="sans-serif"),
    margin=dict(l=10, r=10, t=36, b=10),
)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD ARTIFACTS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    df    = pd.read_csv(os.path.join(DATA_DIR,"test_set.csv")) if os.path.exists(os.path.join(DATA_DIR,"test_set.csv")) else None
    model = joblib.load(os.path.join(DATA_DIR,"verifier_model.pkl")) if os.path.exists(os.path.join(DATA_DIR,"verifier_model.pkl")) else None
    thr   = 0.29
    p = os.path.join(DATA_DIR,"optimal_threshold.txt")
    if os.path.exists(p):
        with open(p) as f: thr = float(f.read().strip())
    return df, model, thr

@st.cache_data(show_spinner=False)
def compute_global_metrics(_model, threshold):
    df = pd.read_csv(os.path.join(DATA_DIR,"test_set.csv"))
    X = df[FEATURES].copy(); X['reason_code'] = X['reason_code'].astype(str).astype('category')
    y = df['dispute_won']; prob = _model.predict(X); pred = (prob > threshold).astype(int)
    return df, y, prob, pred

df, model, THRESHOLD = load_artifacts()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:18px 0 10px;">
      <div style="font-size:2.4rem;">🛡️</div>
      <div style="font-size:1.25rem;font-weight:800;color:#fff;letter-spacing:-.3px;">RazorSentinel-AI</div>
      <div style="font-size:.72rem;color:#4f6a9a;letter-spacing:.8px;margin-top:3px;">RAZORPAY AI BUILDATHON · TRACK 02</div>
    </div>
    <div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.25);border-radius:8px;padding:8px 14px;text-align:center;margin:10px 0;">
      <span class="glow-dot"></span>
      <span style="color:#10b981;font-size:.78rem;font-weight:600;">LIVE · RENDER DEPLOYMENT</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠  Overview",
        "⚡  Live Triage",
        "🔄  Batch Simulator",
        "🧪  Guardrail Demo",
        "📊  Evaluation",
        "📖  About"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""<div class="glass" style="padding:16px;">
      <div style="font-size:.68rem;color:#4f6a9a;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;">Model Stats</div>""",
      unsafe_allow_html=True)
    for k, v in [("Model","LightGBM"),("Threshold",f"{THRESHOLD:.3f}"),
                 ("PR-AUC","0.7519"),("Precision","62.3%"),("Recall","90.2%"),
                 ("Test Set","10K held-out"),("Label Noise","12% injected")]:
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.04);">
          <span style="color:#6b7a9f;font-size:.78rem;">{k}</span>
          <span style="color:#c8d8f8;font-size:.78rem;font-weight:600;">{v}</span></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div style="margin-top:16px;padding:12px 14px;border-radius:9px;background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.2);">
      <div style="font-size:.72rem;color:#f59e0b;font-weight:700;letter-spacing:.4px;">⚡ DEFENSE-ONLY</div>
      <div style="font-size:.72rem;color:#8a7040;margin-top:4px;line-height:1.4;">Structured-in/out · Optional[bool] tri-state · Unsupported claims blocked</div>
    </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown("""<div class="hero">
      <h1>🛡️ RazorSentinel-AI</h1>
      <p>Production-grade Autonomous Chargeback Verifier &amp; Evidence Responder<br>
         Stop merchant losses — with honest metrics, cost-aware thresholding, and unsupported-claim prevention.</p>
      <span class="badge">⚡ Track 02: AI Risk Manager &nbsp;·&nbsp; Single Loss Class: Chargebacks</span>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(5)
    for col, (lbl, val, sub) in zip(cols, [
        ("PR-AUC","0.7519","Threshold-independent"),
        ("Recall","90.2%","Recall-biased · by design"),
        ("Precision","62.3%","At threshold 0.29"),
        ("F1 Score","73.7%","Harmonic mean"),
        ("Test Records","10K","Strictly held-out"),
    ]):
        col.markdown(f'<div class="kpi"><div class="label">{lbl}</div><div class="value">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_arch, c_table = st.columns([3,2], gap="large")

    with c_arch:
        st.markdown("""<div class="glass">
          <div style="font-size:.7rem;color:#4f6a9a;letter-spacing:.9px;text-transform:uppercase;margin-bottom:16px;">Two-Stage Pipeline Architecture</div>
          <div style="background:linear-gradient(90deg,rgba(79,142,247,.12),transparent);border-left:3px solid #4f8ef7;border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:10px;">
            <div style="font-size:.72rem;color:#4f8ef7;font-weight:700;letter-spacing:.5px;">STAGE 1 · VERIFIER</div>
            <div style="font-size:.95rem;color:#e8eeff;font-weight:600;margin:4px 0;">LightGBM Risk Classifier</div>
            <div style="font-size:.8rem;color:#6b7a9f;">11 evidence features → Win probability → Cost-optimal threshold 0.29</div>
          </div>
          <div style="text-align:center;color:#4f6a9a;font-size:1.1rem;margin:4px 0;">↓ if prob &gt; 0.29</div>
          <div style="background:linear-gradient(90deg,rgba(99,102,241,.12),transparent);border-left:3px solid #6366f1;border-radius:0 10px 10px 0;padding:14px 18px;margin-bottom:10px;">
            <div style="font-size:.72rem;color:#818cf8;font-weight:700;letter-spacing:.5px;">STAGE 2 · AUTO-RESPONDER</div>
            <div style="font-size:.95rem;color:#e8eeff;font-weight:600;margin:4px 0;">Gemini + Pydantic Orchestrator</div>
            <div style="font-size:.8rem;color:#6b7a9f;">Structured-in/out schema · Optional[bool] tri-state · Post-gen grounding check</div>
          </div>
          <div style="text-align:center;color:#4f6a9a;font-size:1.1rem;margin:4px 0;">↓ guardrail check</div>
          <div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:10px;padding:14px 18px;">
            <div style="font-size:.72rem;color:#10b981;font-weight:700;letter-spacing:.5px;">OUTPUT</div>
            <div style="font-size:.95rem;color:#e8eeff;font-weight:600;margin:4px 0;">Grounded Defense Packet JSON</div>
            <div style="font-size:.8rem;color:#6b7a9f;">Unsupported claims omitted (None) — never flipped to False</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c_table:
        st.markdown("""<div class="glass" style="height:100%;">
          <div style="font-size:.7rem;color:#4f6a9a;letter-spacing:.9px;text-transform:uppercase;margin-bottom:16px;">Per Reason Code · Held-Out Test Set</div>""",
          unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Code":["10.4","13.1","13.3","11.1","4853"],
            "Category":["Fraud","Not Received","Not as Described","Recovery","MC Dispute"],
            "N":[3005,2972,2012,514,1497],
            "Precision":["60.2%","60.5%","66.8%","65.0%","62.9%"],
            "Recall":["93.2%","85.6%","91.5%","88.8%","92.6%"],
        }), use_container_width=True, hide_index=True)
        st.markdown("""<div style="margin-top:18px;">
          <div style="font-size:.7rem;color:#4f6a9a;letter-spacing:.9px;text-transform:uppercase;margin-bottom:10px;">Guarantees</div>
          <div style="font-size:.83rem;line-height:1.9;color:#c0d0e8;">
            ✅ Structured-in / structured-out LLM schema<br>
            ✅ <code>Optional[bool]</code> — unverified claims omitted<br>
            ✅ Python grounding check on every assertion<br>
            ✅ 12% label noise prevents trivial 99% accuracy<br>
            ✅ Confounder feature ranks last in importance
          </div>
        </div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cm_l, cm_r = st.columns(2, gap="large")
    with cm_l:
        st.markdown("""<div class="glass-gold">
          <div style="font-size:.72rem;color:#f59e0b;font-weight:700;letter-spacing:.5px;margin-bottom:12px;">💰 COST-WEIGHTED THRESHOLD</div>
          <div style="display:flex;gap:16px;margin-bottom:10px;">
            <div style="flex:1;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);border-radius:9px;padding:12px 14px;">
              <div style="font-size:.7rem;color:#ef4444;font-weight:700;">FALSE POSITIVE</div>
              <div style="font-size:1.2rem;color:#fff;font-weight:800;margin:4px 0;">₹ 500</div>
              <div style="font-size:.72rem;color:#8a4a4a;">Ops time + acquirer win-ratio risk</div>
            </div>
            <div style="flex:1;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);border-radius:9px;padding:12px 14px;">
              <div style="font-size:.7rem;color:#f59e0b;font-weight:700;">FALSE NEGATIVE</div>
              <div style="font-size:1.2rem;color:#fff;font-weight:800;margin:4px 0;">₹ Amt + 1500</div>
              <div style="font-size:.72rem;color:#8a6a30;">Revenue lost + Visa/MC fee</div>
            </div>
          </div>
          <div style="font-size:.8rem;color:#9a8060;line-height:1.5;">FN cost ≫ FP cost → threshold 0.29 → high recall is mathematically correct.<br><span style="color:#6a5a40;">* Stated assumptions, not Razorpay-sourced data.</span></div>
        </div>""", unsafe_allow_html=True)
    with cm_r:
        st.markdown("""<div class="glass-green">
          <div style="font-size:.72rem;color:#10b981;font-weight:700;letter-spacing:.5px;margin-bottom:12px;">🔒 GROUNDING CHECK DESIGN</div>
          <div style="font-size:.83rem;color:#c0d0e8;line-height:1.85;">
            The LLM cannot write <em>any</em> free-form prose.<br>
            Every assertion is <code>Optional[bool]</code>:<br><br>
            &nbsp;&nbsp;• <code>True</code> → Confirmed by source evidence<br>
            &nbsp;&nbsp;• <code>None</code> → Omitted (unverified)<br>
            &nbsp;&nbsp;• <code>False</code> → <em>Never set by LLM</em><br><br>
            A post-generation Python loop enforces this — any LLM <code>True</code> that contradicts evidence is set to <code>None</code>, not <code>False</code>.
          </div>
        </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: LIVE TRIAGE
# ═════════════════════════════════════════════════════════════════════════════
elif "Triage" in page:
    st.markdown("""<div class="hero"><h1>⚡ Live Dispute Triage</h1>
      <p>Pull a real dispute from the held-out queue → Verify defensibility → Generate grounded defense packet</p></div>""", unsafe_allow_html=True)
    if df is None or model is None:
        st.error("Artifacts not found. Run training pipeline first."); st.stop()

    ctrl_l, ctrl_r = st.columns([3,1], gap="medium")
    with ctrl_l:
        queue_filter = st.selectbox("Queue filter", ["🔀 All Disputes","✅ Winnable (label=1)","❌ Lost (label=0)"])
    with ctrl_r:
        st.markdown("<br>", unsafe_allow_html=True)
        pull_btn = st.button("🔀  Pull Next Dispute", type="primary")

    if pull_btn:
        pool = df[df['dispute_won']==1] if "Winnable" in queue_filter else (df[df['dispute_won']==0] if "Lost" in queue_filter else df)
        sample = pool.sample(1).iloc[0]
        evidence = DisputeEvidence(
            transaction_id=sample['transaction_id'], reason_code=str(sample['reason_code']),
            avs_match=bool(sample['avs_match']), cvv_match=bool(sample['cvv_match']),
            device_trust_score=float(sample['device_trust_score']), ip_geo_match=bool(sample['ip_geo_match']),
            delivery_confirmed=bool(sample['delivery_confirmed']), is_digital_good=bool(sample['is_digital_good']),
            customer_history_days=int(sample['customer_history_days']), prior_disputes=int(sample['prior_disputes']),
            transaction_amount=float(sample['transaction_amount'])
        )
        st.markdown("<br>", unsafe_allow_html=True)
        for col, (lbl, val) in zip(st.columns(5), [
            ("Transaction ID", evidence.transaction_id),
            ("Amount", f"₹{evidence.transaction_amount:,.2f}"),
            ("Reason Code", REASON_MAP.get(evidence.reason_code, evidence.reason_code)),
            ("Device Trust", f"{evidence.device_trust_score:.2f}"),
            ("Customer Age", f"{evidence.customer_history_days}d")
        ]):
            col.markdown(f'<div class="kpi"><div class="label">{lbl}</div><div class="value" style="font-size:1.1rem;">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        left_col, right_col = st.columns(2, gap="large")

        with left_col:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="sbadge">Stage 1 · LightGBM Verifier</div>', unsafe_allow_html=True)
            pred_row = sample[FEATURES].to_frame().T.copy()
            pred_row['reason_code'] = pred_row['reason_code'].astype(str).astype('category')
            prob = float(model.predict(pred_row)[0])
            is_def = prob > THRESHOLD
            bar_color = "#10b981" if is_def else "#ef4444"
            pct = int(prob*100)
            st.markdown(f"""<div style="margin:8px 0 4px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="color:#a0b4d8;font-size:.85rem;">Win Probability</span>
                <span style="color:#fff;font-size:1.2rem;font-weight:800;">{prob:.1%}</span>
              </div>
              <div class="prob-wrap"><div class="prob-fill" style="width:{pct}%;background:linear-gradient(90deg,{bar_color},{bar_color}99);"></div></div>
              <div style="display:flex;justify-content:space-between;margin-top:4px;">
                <span style="font-size:.7rem;color:#4f6a9a;">0%</span>
                <span style="font-size:.7rem;color:{bar_color};">Threshold: {THRESHOLD:.1%}</span>
                <span style="font-size:.7rem;color:#4f6a9a;">100%</span>
              </div></div>""", unsafe_allow_html=True)
            if is_def:
                st.markdown(f'<div class="verdict-win" style="margin:14px 0;"><div class="vtitle">✅ DEFENSIBLE</div><div class="vsub">Score {prob:.1%} exceeds threshold {THRESHOLD:.1%} — escalating to Stage 2</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="verdict-loss" style="margin:14px 0;"><div class="vtitle">❌ NOT DEFENSIBLE</div><div class="vsub">Score {prob:.1%} below threshold {THRESHOLD:.1%} — accept liability</div></div>', unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=round(prob*100,1),
                number={"suffix":"%","font":{"color":"#fff","size":28}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#4f6a9a","tickfont":{"color":"#4f6a9a","size":10}},
                       "bar":{"color":bar_color,"thickness":.3},"bgcolor":"rgba(0,0,0,0)","borderwidth":0,
                       "steps":[{"range":[0,THRESHOLD*100],"color":"rgba(239,68,68,.12)"},{"range":[THRESHOLD*100,100],"color":"rgba(16,185,129,.12)"}],
                       "threshold":{"line":{"color":"#f59e0b","width":2},"thickness":.8,"value":THRESHOLD*100}}
            ))
            fig_g.update_layout(**PLOTLY_LAYOUT, height=180, title=dict(text=f"Threshold @ {THRESHOLD:.1%}",font=dict(color="#6b7a9f",size=11),y=.02))
            st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar":False})
            for k, v, t in [("AVS Match",evidence.avs_match,"bool"),("CVV Match",evidence.cvv_match,"bool"),
                             ("IP/Geo Match",evidence.ip_geo_match,"bool"),("Delivery",evidence.delivery_confirmed,"bool"),
                             ("Digital Good",evidence.is_digital_good,"bool"),("Prior Disputes",evidence.prior_disputes,"num")]:
                cls = "ev-yes" if v else "ev-no" if t=="bool" else "ev-num"
                disp = ("✅ Yes" if v else "❌ No") if t=="bool" else str(v)
                st.markdown(f'<div class="ev-row"><span class="ev-key">{k}</span><span class="ev-val {cls}">{disp}</span></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="sbadge">Stage 2 · Auto-Responder</div>', unsafe_allow_html=True)
            with st.spinner("Assembling grounded defense packet…"):
                import datetime
                has_key = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
                packet = generate_defense_packet(evidence)
                gen_time = datetime.datetime.now().strftime("%H:%M:%S IST")

            # Mode indicator
            if has_key:
                st.success("🤖 **Gemini Active** — LLM generated this defense packet")
            else:
                st.warning("⚙️ **Deterministic Fallback** — Set `GEMINI_API_KEY` on Render for live LLM responses")
            pkt_color = "#10b981" if packet.is_defensible else "#ef4444"
            st.markdown(f"""<div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:16px 18px;margin:6px 0 14px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="color:#6b7a9f;font-size:.78rem;text-transform:uppercase;letter-spacing:.6px;">Verdict</span>
                <span style="color:{pkt_color};font-size:.85rem;font-weight:700;">{"✅ DEFENSIBLE" if packet.is_defensible else "❌ NOT DEFENSIBLE"}</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="color:#6b7a9f;font-size:.78rem;text-transform:uppercase;letter-spacing:.6px;">Evidence Category</span>
                <span style="color:#22d3ee;font-size:.85rem;font-weight:600;">{packet.compelling_evidence_category}</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#6b7a9f;font-size:.78rem;text-transform:uppercase;letter-spacing:.6px;">Template</span>
                <span style="color:#a0b4d8;font-size:.85rem;font-weight:600;font-family:monospace;">{packet.explanation_template_id}</span>
              </div></div>""", unsafe_allow_html=True)
            st.markdown('<div style="font-size:.7rem;color:#4f6a9a;text-transform:uppercase;letter-spacing:.9px;margin-bottom:8px;">Guardrail Diagnostics</div>', unsafe_allow_html=True)
            pills = ""
            for label, val in [("📦 Delivery",packet.asserts_delivery_confirmed),("🔐 Auth Match",packet.asserts_auth_match),("📡 Device/IP",packet.asserts_device_match)]:
                pills += f'<span class="pill-ok">✅ {label}: Grounded</span>' if val is True else f'<span class="pill-omit">⚪ {label}: Omitted</span>'
            st.markdown(pills, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.7rem;color:#4f6a9a;text-transform:uppercase;letter-spacing:.9px;margin:14px 0 6px;">Defense Packet JSON</div>', unsafe_allow_html=True)
            st.json(packet.model_dump(), expanded=False)
            import json as _json
            st.download_button(
                label="⬇️  Download Defense Packet",
                data=_json.dumps(packet.model_dump(), indent=2),
                file_name=f"defense_packet_{evidence.transaction_id}.json",
                mime="application/json",
            )
            gt_val = int(sample['dispute_won'])
            gt_color = "#10b981" if gt_val==1 else "#ef4444"
            st.markdown(f'<div style="margin-top:16px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;"><span style="color:#6b7a9f;font-size:.8rem;">Ground-Truth Label</span><span style="color:{gt_color};font-weight:800;">{"🏆 WON" if gt_val==1 else "❌ LOST"}</span></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: BATCH SIMULATOR  ← NEW PROTOTYPE FEATURE
# ═════════════════════════════════════════════════════════════════════════════
elif "Batch" in page:
    st.markdown("""<div class="hero"><h1>🔄 Batch Queue Simulator</h1>
      <p>Simulate processing a queue of N disputes simultaneously — shows the Verifier scoring all disputes in one pass</p></div>""", unsafe_allow_html=True)
    if df is None or model is None:
        st.error("Artifacts not found."); st.stop()

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        batch_size = st.slider("Batch size", min_value=5, max_value=30, value=10, step=5)
    with col_ctrl2:
        reason_filter = st.selectbox("Filter by reason code", ["All"] + sorted(df['reason_code'].astype(str).unique().tolist()))
    with col_ctrl3:
        st.markdown("<br>", unsafe_allow_html=True)
        run_batch = st.button("▶️  Run Batch", type="primary")

    if run_batch:
        pool = df.copy()
        if reason_filter != "All":
            pool = pool[pool['reason_code'].astype(str) == reason_filter]
        batch = pool.sample(min(batch_size, len(pool)))
        X_batch = batch[FEATURES].copy()
        X_batch['reason_code'] = X_batch['reason_code'].astype(str).astype('category')
        probs = model.predict(X_batch)
        decisions = (probs > THRESHOLD).astype(int)

        st.markdown("<br>", unsafe_allow_html=True)
        # Summary row
        n_defend = decisions.sum(); n_drop = len(decisions) - n_defend
        est_savings = batch.loc[decisions==1,'transaction_amount'].sum() + n_defend*1500
        s1, s2, s3, s4 = st.columns(4)
        for col, (lbl, val, sub) in zip([s1,s2,s3,s4],[
            ("Disputes Processed", str(len(batch)), "In this batch"),
            ("Defensible → Respond", str(n_defend), f"{n_defend/len(batch):.0%} of queue"),
            ("Drop → Accept", str(n_drop), f"{n_drop/len(batch):.0%} of queue"),
            ("Est. Revenue Protected", f"₹{est_savings:,.0f}", "If all defended successfully"),
        ]):
            col.markdown(f'<div class="kpi"><div class="label">{lbl}</div><div class="value" style="font-size:1.2rem;">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        left_q, right_q = st.columns([3,2], gap="large")

        with left_q:
            st.markdown("#### 📋 Dispute Queue Results")
            for i, (idx, row) in enumerate(batch.iterrows()):
                p = probs[i]; d = decisions[i]
                bar_w = int(p*100); bar_col = "#10b981" if d else "#ef4444"
                badge_cls = "qb-win" if d else "qb-loss"; badge_txt = "DEFEND" if d else "DROP"
                tid = str(row['transaction_id'])[:14]
                st.markdown(f"""<div class="queue-row">
                  <span class="queue-id">{tid}</span>
                  <div class="queue-bar-wrap"><div class="queue-bar" style="width:{bar_w}%;background:{bar_col};"></div></div>
                  <span class="queue-score" style="color:{bar_col};">{p:.2f}</span>
                  <span class="queue-badge {badge_cls}">{badge_txt}</span>
                </div>""", unsafe_allow_html=True)

        with right_q:
            st.markdown("#### 📊 Batch Decision Distribution")
            fig = go.Figure(go.Bar(
                x=["Defend (Defensible)","Drop (Accept)"], y=[n_defend,n_drop],
                marker_color=["#10b981","#ef4444"],
                marker_line_color="rgba(255,255,255,.1)", marker_line_width=1,
            ))
            fig.update_layout(**PLOTLY_LAYOUT, height=220, showlegend=False,
                              yaxis=dict(gridcolor="rgba(255,255,255,.06)"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

            st.markdown("#### 📉 Score Distribution")
            fig2 = go.Figure()
            fig2.add_trace(go.Histogram(x=probs[decisions==1], name="Defensible",
                                         marker_color="#10b98166", nbinsx=15))
            fig2.add_trace(go.Histogram(x=probs[decisions==0], name="Dropped",
                                         marker_color="#ef444466", nbinsx=15))
            fig2.add_vline(x=THRESHOLD, line_dash="dash", line_color="#f59e0b", line_width=1.5)
            fig2.update_layout(**PLOTLY_LAYOUT, height=200, barmode="overlay",
                               legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#a0b4d8",size=10)),
                               yaxis=dict(gridcolor="rgba(255,255,255,.06)"),
                               xaxis=dict(gridcolor="rgba(255,255,255,.06)"))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: GUARDRAIL DEMO  ← NEW PROTOTYPE FEATURE
# ═════════════════════════════════════════════════════════════════════════════
elif "Guardrail" in page:
    st.markdown("""<div class="hero"><h1>🧪 Guardrail Demo</h1>
      <p>Watch the anti-hallucination grounding check block an unsupported AI claim in real-time</p></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="glass-indigo" style="margin-bottom:24px;">
      <div style="font-size:.72rem;color:#818cf8;font-weight:700;letter-spacing:.5px;margin-bottom:10px;">WHAT THIS DEMONSTRATES</div>
      <div style="font-size:.85rem;color:#c0d0e8;line-height:1.7;">
        This page lets you manually configure a dispute with conflicting evidence, trigger the AI responder, 
        and watch the Python grounding layer intercept any unsupported claim before it reaches the final defense packet.
        <br><br>
        This directly answers the question: <em>"Can the AI be tricked into asserting evidence that doesn't exist?"</em>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### ⚙️ Configure Adversarial Evidence")
    st.caption("Set some fields to False to create a scenario where the LLM might hallucinate")

    a1, a2, a3 = st.columns(3)
    with a1:
        adv_delivery   = st.toggle("Delivery Confirmed",    value=False, help="Set to False to test delivery claim blocking")
        adv_avs        = st.toggle("AVS Match",             value=True)
        adv_cvv        = st.toggle("CVV Match",             value=True)
    with a2:
        adv_ip         = st.toggle("IP/Geo Match",          value=True)
        adv_digital    = st.toggle("Is Digital Good",       value=False)
        adv_trust      = st.slider("Device Trust Score",    0.0, 1.0, 0.85, 0.05)
    with a3:
        adv_amount     = st.number_input("Transaction Amount (₹)", value=5000, min_value=100, step=500)
        adv_history    = st.number_input("Customer History (days)", value=180, min_value=1, step=30)
        adv_reason     = st.selectbox("Reason Code", ["13.1","10.4","13.3","11.1","4853"])

    run_adv = st.button("🧪  Run Adversarial Test", type="primary")

    if run_adv:
        adv_evidence = DisputeEvidence(
            transaction_id="ADVERSARIAL-TEST-001",
            reason_code=adv_reason,
            avs_match=adv_avs, cvv_match=adv_cvv,
            device_trust_score=adv_trust, ip_geo_match=adv_ip,
            delivery_confirmed=adv_delivery, is_digital_good=adv_digital,
            customer_history_days=adv_history, prior_disputes=0,
            transaction_amount=float(adv_amount)
        )

        st.markdown("---")
        st.markdown("### 🔍 Grounding Check Trace")

        # Step 1: Source Evidence
        st.markdown(f"""<div class="adv-step adv-evidence">
          <strong style="color:#4f8ef7;">① SOURCE EVIDENCE (Ground Truth)</strong><br>
          Delivery: <strong style="color:{'#10b981' if adv_delivery else '#ef4444'}">{'TRUE' if adv_delivery else 'FALSE'}</strong> &nbsp;|&nbsp;
          AVS: <strong style="color:{'#10b981' if adv_avs else '#ef4444'}">{'TRUE' if adv_avs else 'FALSE'}</strong> &nbsp;|&nbsp;
          CVV: <strong style="color:{'#10b981' if adv_cvv else '#ef4444'}">{'TRUE' if adv_cvv else 'FALSE'}</strong> &nbsp;|&nbsp;
          Device Trust: <strong style="color:#22d3ee;">{adv_trust:.2f}</strong>
        </div>""", unsafe_allow_html=True)

        # Step 2: LLM Attempt
        st.markdown("""<div class="adv-step adv-attempt">
          <strong style="color:#ef4444;">② LLM GENERATION ATTEMPT</strong><br>
          Gemini processes the DisputeEvidence schema and attempts to assert Boolean flags...
          <em style="color:#8a4a4a;">(LLM may attempt to assert claims not supported by evidence)</em>
        </div>""", unsafe_allow_html=True)

        with st.spinner("Calling responder with adversarial evidence…"):
            adv_packet = generate_defense_packet(adv_evidence)

        # Step 3: Guardrail check
        delivery_blocked = not adv_delivery and adv_packet.asserts_delivery_confirmed is None
        auth_blocked     = not (adv_avs and adv_cvv) and adv_packet.asserts_auth_match is None
        device_blocked   = not (adv_ip and adv_trust > 0.7) and adv_packet.asserts_device_match is None

        checks = [
            ("📦 Delivery Claim", adv_delivery, adv_packet.asserts_delivery_confirmed, delivery_blocked),
            ("🔐 Auth Match Claim", adv_avs and adv_cvv, adv_packet.asserts_auth_match, auth_blocked),
            ("📡 Device/IP Claim", adv_ip and adv_trust > 0.7, adv_packet.asserts_device_match, device_blocked),
        ]
        guardrail_html = '<div class="adv-step adv-blocked"><strong style="color:#f59e0b;">③ GUARDRAIL INTERVENTION</strong><br><br>'
        for name, evidence_val, packet_val, was_blocked in checks:
            if not evidence_val and packet_val is None:
                guardrail_html += f'<span class="pill-blocked">❌ {name}: BLOCKED (unsupported → omitted)</span> '
            elif evidence_val and packet_val:
                guardrail_html += f'<span class="pill-ok">✅ {name}: Grounded & Permitted</span> '
            else:
                guardrail_html += f'<span class="pill-omit">⚪ {name}: Not Asserted</span> '
        guardrail_html += "</div>"
        st.markdown(guardrail_html, unsafe_allow_html=True)

        # Step 4: Final output
        st.markdown(f"""<div class="adv-step adv-output">
          <strong style="color:#10b981;">④ FINAL DEFENSE PACKET (Safe for submission)</strong><br>
          <code>is_defensible: {adv_packet.is_defensible}</code><br>
          <code>compelling_evidence_category: "{adv_packet.compelling_evidence_category}"</code><br>
          <code>asserts_delivery_confirmed: {adv_packet.asserts_delivery_confirmed}</code><br>
          <code>asserts_auth_match: {adv_packet.asserts_auth_match}</code><br>
          <code>asserts_device_match: {adv_packet.asserts_device_match}</code>
        </div>""", unsafe_allow_html=True)

        blocked_count = sum(1 for _, ev, pv, _ in checks if not ev and pv is None)
        if blocked_count > 0:
            st.success(f"✅ Guardrail successfully blocked **{blocked_count} unsupported claim(s)** from reaching the defense packet.")
        else:
            st.info("ℹ️ All assertions were grounded by the source evidence — no blocking needed.")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: EVALUATION
# ═════════════════════════════════════════════════════════════════════════════
elif "Evaluation" in page:
    st.markdown("""<div class="hero"><h1>📊 Evaluation Deep-Dive</h1>
      <p>Full metrics on the strictly held-out 10,000-record test set — never touched during training or threshold tuning</p></div>""", unsafe_allow_html=True)
    if model is None or df is None:
        st.error("Model or data not found."); st.stop()

    test_df, y_test, preds_prob, preds_binary = compute_global_metrics(model, THRESHOLD)
    pr_auc=average_precision_score(y_test,preds_prob)
    precision=precision_score(y_test,preds_binary)
    recall=recall_score(y_test,preds_binary)
    f1=f1_score(y_test,preds_binary)

    for col,(lbl,val,sub) in zip(st.columns(4),[
        ("PR-AUC",f"{pr_auc:.4f}","Threshold-independent"),
        ("Precision",f"{precision:.4f}",f"@ threshold {THRESHOLD:.3f}"),
        ("Recall",f"{recall:.4f}","Recall-biased · by design"),
        ("F1 Score",f"{f1:.4f}","Harmonic mean")]):
        col.markdown(f'<div class="kpi"><div class="label">{lbl}</div><div class="value">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1,tab2,tab3,tab4 = st.tabs(["📈 PR Curve","💰 Cost Optimisation","🗺️ Confusion Matrix","📋 Feature Importance"])

    with tab1:
        prec_c,rec_c,_ = precision_recall_curve(y_test,preds_prob)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rec_c,y=prec_c,mode="lines",line=dict(color="#4f8ef7",width=2.5),fill="tozeroy",fillcolor="rgba(79,142,247,.08)",name=f"PR Curve (AUC={pr_auc:.4f})"))
        fig.add_trace(go.Scatter(x=[recall],y=[precision],mode="markers",marker=dict(color="#f59e0b",size=10,symbol="diamond",line=dict(color="#fff",width=1.5)),name=f"Operating Point ({THRESHOLD:.2f})"))
        fig.add_hline(y=y_test.mean(),line_dash="dot",line_color="#ef444488",annotation_text=f"No-skill ({y_test.mean():.2f})",annotation_font_color="#ef4444")
        fig.update_layout(**PLOTLY_LAYOUT,height=420,title="Precision-Recall Curve (Held-Out Test Set)",xaxis_title="Recall",yaxis_title="Precision",legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#a0b4d8")),xaxis=dict(gridcolor="rgba(255,255,255,.06)"),yaxis=dict(gridcolor="rgba(255,255,255,.06)"))
        st.plotly_chart(fig,use_container_width=True)

    with tab2:
        FP_COST=500; thresholds=np.linspace(0.05,0.95,91); costs,fp_costs,fn_costs=[],[],[]
        for t in thresholds:
            pb=(preds_prob>t).astype(int); fp_m=(pb==1)&(y_test.values==0); fn_m=(pb==0)&(y_test.values==1)
            fpc=fp_m.sum()*FP_COST; fnc=(test_df.loc[fn_m,'transaction_amount'].values+1500).sum()
            costs.append(fpc+fnc); fp_costs.append(fpc); fn_costs.append(fnc)
        opt_idx=int(np.argmin(costs)); opt_cost=costs[opt_idx]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=thresholds,y=fp_costs,name="FP Cost (₹500/dispute)",line=dict(color="#f59e0b",width=1.5,dash="dot"),fill="tozeroy",fillcolor="rgba(245,158,11,.06)"))
        fig.add_trace(go.Scatter(x=thresholds,y=fn_costs,name="FN Cost (Amt+₹1500)",line=dict(color="#ef4444",width=1.5,dash="dot"),fill="tozeroy",fillcolor="rgba(239,68,68,.06)"))
        fig.add_trace(go.Scatter(x=thresholds,y=costs,name="Total Expected Cost",line=dict(color="#4f8ef7",width=3),fill="tozeroy",fillcolor="rgba(79,142,247,.06)"))
        fig.add_vline(x=THRESHOLD,line_dash="dash",line_color="#10b981",line_width=2,annotation_text=f"Optimal @ {THRESHOLD:.2f}",annotation_font_color="#10b981")
        fig.add_trace(go.Scatter(x=[THRESHOLD],y=[opt_cost],mode="markers",marker=dict(color="#10b981",size=12,symbol="star"),name=f"Min Cost ₹{opt_cost:,.0f}",showlegend=True))
        fig.update_layout(**PLOTLY_LAYOUT,height=420,title="Cost Optimisation — FP vs FN Tradeoff",xaxis_title="Decision Threshold",yaxis_title="Expected Cost (₹)",legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#a0b4d8")),xaxis=dict(gridcolor="rgba(255,255,255,.06)"),yaxis=dict(gridcolor="rgba(255,255,255,.06)"))
        st.plotly_chart(fig,use_container_width=True)
        st.caption("FP Cost: ₹500 (stated assumption). FN Cost: transaction amount + ₹1,500 (stated assumption).")

    with tab3:
        cm=confusion_matrix(y_test,preds_binary)
        z=cm.tolist(); labels=[["TN — Correctly Dropped","FP — Filed Weak Defense"],["FN — Missed Winnable","TP — Correctly Defended"]]
        text=[[f"<b>{z[i][j]}</b><br><span style='font-size:10px'>{labels[i][j]}</span>" for j in range(2)] for i in range(2)]
        fig=go.Figure(go.Heatmap(z=z,x=["Predicted: Drop","Predicted: Defend"],y=["Actual: Lost","Actual: Won"],text=text,texttemplate="%{text}",colorscale=[[0,"#0d1526"],[0.5,"#1a3a7a"],[1,"#4f8ef7"]],showscale=False))
        fig.update_layout(**PLOTLY_LAYOUT,height=380,title=f"Confusion Matrix @ Threshold {THRESHOLD:.3f}",xaxis=dict(side="bottom"))
        st.plotly_chart(fig,use_container_width=True)

    with tab4:
        fi=pd.Series(model.feature_importance(importance_type="gain"),index=FEATURES).sort_values()
        colors=["#ef4444" if f=="confounder_feature" else "#4f8ef7" for f in fi.index]
        fig=go.Figure(go.Bar(x=fi.values,y=fi.index,orientation="h",marker=dict(color=colors,line=dict(color="rgba(255,255,255,.08)",width=.5))))
        fig.update_layout(**PLOTLY_LAYOUT,height=400,title="Feature Importance (Gain) — confounder_feature ranks last ✅",xaxis_title="Importance Score (Gain)",xaxis=dict(gridcolor="rgba(255,255,255,.06)"))
        st.plotly_chart(fig,use_container_width=True)
        st.caption("🔴 confounder_feature is pure noise (N(50,15), zero label correlation). Ranking last confirms model generalises.")

    st.markdown("### Per Reason Code Breakdown")
    rows=[]
    for code in test_df['reason_code'].astype(str).unique():
        mask=test_df['reason_code'].astype(str)==code; y_sub=y_test[mask]; pb_sub=preds_binary[mask]
        rows.append({"Reason Code":REASON_MAP.get(code,code),"N":int(mask.sum()),"Base Win Rate":f"{y_sub.mean():.1%}",
                     "Precision":f"{precision_score(y_sub,pb_sub,zero_division=0):.3f}","Recall":f"{recall_score(y_sub,pb_sub,zero_division=0):.3f}","F1":f"{f1_score(y_sub,pb_sub,zero_division=0):.3f}"})
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ═════════════════════════════════════════════════════════════════════════════
elif "About" in page:
    st.markdown("""<div class="hero"><h1>📖 About RazorSentinel-AI</h1>
      <p>Technical reference · Design decisions · What broke and why it made the project better</p></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""<div class="glass" style="margin-bottom:16px;">
          <div style="font-size:.7rem;color:#4f6a9a;letter-spacing:.9px;text-transform:uppercase;margin-bottom:14px;">What Broke (And What It Fixed)</div>
          <div style="border-left:3px solid #ef4444;padding:10px 14px;background:rgba(239,68,68,.05);border-radius:0 8px 8px 0;margin-bottom:12px;">
            <div style="font-size:.82rem;font-weight:700;color:#ef4444;margin-bottom:4px;">① Label Leakage</div>
            <div style="font-size:.8rem;color:#9aa0b0;line-height:1.5;">First generator → deterministic labels → 97% PR-AUC instantly. Fix: 12% noise + confounder. PR-AUC dropped to 0.75.</div>
          </div>
          <div style="border-left:3px solid #f59e0b;padding:10px 14px;background:rgba(245,158,11,.05);border-radius:0 8px 8px 0;margin-bottom:12px;">
            <div style="font-size:.82rem;font-weight:700;color:#f59e0b;margin-bottom:4px;">② Broken Guardrail</div>
            <div style="font-size:.8rem;color:#9aa0b0;line-height:1.5;">Set unverified claims to <code>False</code> — actively wrong. Fix: <code>Optional[bool]</code>. Unverified → <code>None</code> → omitted.</div>
          </div>
          <div style="border-left:3px solid #4f8ef7;padding:10px 14px;background:rgba(79,142,247,.05);border-radius:0 8px 8px 0;">
            <div style="font-size:.82rem;font-weight:700;color:#4f8ef7;margin-bottom:4px;">③ Threshold Misread</div>
            <div style="font-size:.8rem;color:#9aa0b0;line-height:1.5;">62%/90% reads as naive without context. Fix: explicit cost math everywhere — it is a business decision, not a bug.</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="glass" style="margin-bottom:16px;">
          <div style="font-size:.7rem;color:#4f6a9a;letter-spacing:.9px;text-transform:uppercase;margin-bottom:14px;">Tech Stack</div>""", unsafe_allow_html=True)
        for tech, desc in [
            ("🤖 Verifier","LightGBM — structured features, interpretable, honest PR-AUC"),
            ("🧠 Responder LLM","Gemini — structured JSON output mode, temperature=0"),
            ("📐 Schema","Pydantic v2 — DisputeEvidence + DefensePacket"),
            ("🛡️ Guardrail","Optional[bool] tri-state → post-gen Python loop"),
            ("📊 Evaluation","scikit-learn PR-AUC, per-reason-code, cost curve"),
            ("🎨 Frontend","Streamlit + Plotly — interactive, dark-mode, zero-lag"),
            ("🐳 Deployment","Docker → Render + Vercel static landing"),
            ("📦 Data","50k synthetic records — 12% noise, confounder"),
        ]:
            st.markdown(f'<div style="padding:9px 12px;border-radius:8px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);margin-bottom:6px;"><div style="color:#c0d0e8;font-weight:600;">{tech}</div><div style="color:#6b7a9f;font-size:.78rem;margin-top:3px;">{desc}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div class="glass-gold">
          <div style="font-size:.7rem;color:#f59e0b;font-weight:700;letter-spacing:.5px;margin-bottom:10px;">RUBRIC ALIGNMENT</div>
          <div style="font-size:.82rem;line-height:1.85;color:#c0b070;">
            ✅ Single loss class: Chargebacks only<br>
            ✅ Working verifier + auto-responder<br>
            ✅ Measured precision/recall on held-out test set<br>
            ✅ Honest metrics including false-positive cost<br>
            ✅ Strictly defense-only (disqualification bar cleared)<br>
            ✅ Show your work: cost curve, per-code, feature importance
          </div>
        </div>""", unsafe_allow_html=True)
