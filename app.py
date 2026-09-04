import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    average_precision_score, confusion_matrix,
    precision_recall_curve
)
from src.schemas import DisputeEvidence
from src.responder import generate_defense_packet

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RazorSentinel-AI",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- header strip ---- */
.hero {
    background: linear-gradient(135deg, #1a56ff 0%, #0a0e1a 60%);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
}
.hero h1 { color: #fff; font-size: 2.2rem; margin: 0 0 4px; }
.hero p  { color: #a0b4ff; font-size: 1rem; margin: 0; }

/* ---- stage badge ---- */
.stage-badge {
    display: inline-block;
    background: #1a56ff22;
    border: 1px solid #1a56ff88;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #6fa0ff;
    letter-spacing: .5px;
    margin-bottom: 10px;
}

/* ---- metric card ---- */
.metric-card {
    background: #1a1d24;
    border: 1px solid #2a2d3a;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
}
.metric-card .label { font-size: 0.75rem; color: #7a8aaa; text-transform: uppercase; letter-spacing: .8px; }
.metric-card .value { font-size: 1.7rem; font-weight: 700; color: #e8ecff; margin-top: 4px; }
.metric-card .sub   { font-size: 0.75rem; color: #5a6880; margin-top: 2px; }

/* ---- verdict strip ---- */
.verdict-win  { background:#0d2a1a; border-left:4px solid #00d26a; border-radius:8px; padding:14px 18px; }
.verdict-loss { background:#2a0d0d; border-left:4px solid #ff4444; border-radius:8px; padding:14px 18px; }
.verdict-win  span { color:#00d26a; font-weight:700; font-size:1.1rem; }
.verdict-loss span { color:#ff4444; font-weight:700; font-size:1.1rem; }

/* ---- guardrail pill ---- */
.pill-ok   { display:inline-block; background:#0d2a1a; border:1px solid #00d26a; border-radius:20px;
             padding:3px 12px; color:#00d26a; font-size:0.8rem; margin:3px 2px; }
.pill-omit { display:inline-block; background:#1e2030; border:1px solid #3a3d4a; border-radius:20px;
             padding:3px 12px; color:#606880; font-size:0.8rem; margin:3px 2px; }

/* ---- table ---- */
.metrics-table th { color:#7a8aaa !important; font-size:0.78rem; }
.metrics-table td { font-size:0.88rem; }

/* ---- hide streamlit chrome ---- */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Load artifacts ────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

REASON_LABELS = {
    "10.4":  "10.4 — Fraud (Card Absent)",
    "13.1":  "13.1 — Merchandise Not Received",
    "13.3":  "13.3 — Not as Described",
    "11.1":  "11.1 — Card Recovery Bulletin",
    "4853":  "4853 — Cardholder Dispute (MC)",
    "4853.0":"4853 — Cardholder Dispute (MC)",
}

@st.cache_resource(show_spinner=False)
def load_artifacts():
    test_path  = os.path.join(DATA_DIR, "test_set.csv")
    model_path = os.path.join(DATA_DIR, "verifier_model.pkl")
    thr_path   = os.path.join(DATA_DIR, "optimal_threshold.txt")

    df    = pd.read_csv(test_path) if os.path.exists(test_path) else None
    model = joblib.load(model_path) if os.path.exists(model_path) else None
    thr   = 0.29
    if os.path.exists(thr_path):
        with open(thr_path) as f:
            thr = float(f.read().strip())
    return df, model, thr

df, model, THRESHOLD = load_artifacts()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ RazorSentinel-AI")
    st.caption("Razorpay AI Buildathon · Track 02")
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio("", ["🏠 Overview & Metrics", "⚡ Live Dispute Triage", "📊 Evaluation Deep-Dive"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Model:** LightGBM Verifier")
    st.markdown(f"**Decision Threshold:** `{THRESHOLD:.3f}` *(cost-optimal)*")
    st.markdown("**PR-AUC:** `0.7519`")
    st.markdown("**Precision:** `62.3%`  **Recall:** `90.2%`")
    st.markdown("---")
    st.caption("Defense-only · Zero hallucination · Pydantic v2")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview & Metrics":
    st.markdown("""
    <div class="hero">
      <h1>🛡️ RazorSentinel-AI</h1>
      <p>Autonomous Chargeback Verifier &amp; Evidence Responder &nbsp;·&nbsp;
         Razorpay AI Buildathon · Track 02: AI Risk Manager</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top KPIs ──
    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        ("PR-AUC",       "0.7519", "Threshold-independent"),
        ("Precision",    "62.3%",  "@ threshold 0.29"),
        ("Recall",       "90.2%",  "Recall-biased by design"),
        ("F1 Score",     "73.7%",  "Harmonic mean"),
        ("Test Records", "10,000", "Strictly held-out"),
    ]
    for col, (label, val, sub) in zip([c1,c2,c3,c4,c5], kpis):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{val}</div>
            <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Architecture ──
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("### 🏗️ Two-Stage Architecture")
        st.markdown("""
**Stage 1 — Verifier (LightGBM)**
Classifies each incoming dispute as *defensible* or *not defensible* using 11 structured evidence features (AVS/CVV match, device trust score, IP/geo, delivery confirmation, Visa/MC reason code). Trained on 30,000 records, tuned on 10,000 — evaluated on a strictly held-out 10,000 never touched during threshold selection.

**Stage 2 — Auto-Responder (Gemini + Pydantic)**
For defensible disputes, an LLM selects evidence flags from a fixed Pydantic schema. It cannot write free-form prose. A Python post-generation guardrail drops any flag to `None` (omitted) if the source evidence does not explicitly support it — meaning the system never asserts the *opposite* of truth, it simply omits the claim.

**Cost-Weighted Threshold**
FP Cost = ₹500 (wasted ops + win-ratio risk). FN Cost = transaction amount + ₹1,500 (assumed Visa/MC fee). The threshold 0.29 is mathematically optimal on the validation set for minimising total expected business loss — intentionally recall-biased.
        """)

    with col_b:
        st.markdown("### 📋 Per Reason Code (Held-Out)")
        table_data = {
            "Reason Code": ["10.4 Fraud", "13.1 Not Received", "13.3 Not as Described", "11.1 Recovery", "4853 MC Dispute"],
            "N":           [3005, 2972, 2012, 514, 1497],
            "Precision":   ["60.2%", "60.5%", "66.8%", "65.0%", "62.9%"],
            "Recall":      ["93.2%", "85.6%", "91.5%", "88.8%", "92.6%"],
        }
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        st.markdown("### 🔒 Defense-Only Guarantees")
        st.markdown("""
- ✅ Structured-in / structured-out LLM schema  
- ✅ `Optional[bool]` tri-state — never flip unverified to `False`  
- ✅ Python guardrail validates every LLM assertion  
- ✅ 12% label noise prevents trivial 99% accuracy  
- ✅ Pure confounder feature verifies model generalises  
        """)

    # ── Cost curve image ──
    st.markdown("### 📉 Cost Optimisation Curve")
    cost_img = os.path.join(DATA_DIR, "cost_curve.png")
    cm_img   = os.path.join(DATA_DIR, "confusion_matrix.png")
    if os.path.exists(cost_img) and os.path.exists(cm_img):
        ci1, ci2 = st.columns(2)
        ci1.image(cost_img, caption="Total Expected Cost (FP+FN) vs Decision Threshold", use_container_width=True)
        ci2.image(cm_img,   caption="Confusion Matrix @ Optimal Threshold 0.29", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — LIVE TRIAGE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Live Dispute Triage":
    st.markdown("""
    <div class="hero">
      <h1>⚡ Live Dispute Triage</h1>
      <p>Pull a dispute from the held-out queue · run the Verifier · generate a grounded defense packet</p>
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.error("Test dataset not found. Run the training pipeline first.")
        st.stop()

    FEATURES = [
        'transaction_amount','avs_match','cvv_match','device_trust_score',
        'ip_geo_match','delivery_confirmed','is_digital_good',
        'customer_history_days','prior_disputes','confounder_feature','reason_code'
    ]

    filter_col, btn_col = st.columns([3, 1])
    with filter_col:
        queue_filter = st.selectbox(
            "Filter queue by ground-truth label:",
            ["All Disputes", "Only Winnable (label=1)", "Only Lost (label=0)"],
        )
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        load_btn = st.button("🔀 Pull Next Dispute", type="primary", use_container_width=True)

    if load_btn:
        if queue_filter == "Only Winnable (label=1)":
            pool = df[df['dispute_won'] == 1]
        elif queue_filter == "Only Lost (label=0)":
            pool = df[df['dispute_won'] == 0]
        else:
            pool = df
        sample = pool.sample(1).iloc[0]

        evidence = DisputeEvidence(
            transaction_id    = sample['transaction_id'],
            reason_code       = str(sample['reason_code']),
            avs_match         = bool(sample['avs_match']),
            cvv_match         = bool(sample['cvv_match']),
            device_trust_score= float(sample['device_trust_score']),
            ip_geo_match      = bool(sample['ip_geo_match']),
            delivery_confirmed= bool(sample['delivery_confirmed']),
            is_digital_good   = bool(sample['is_digital_good']),
            customer_history_days=int(sample['customer_history_days']),
            prior_disputes    = int(sample['prior_disputes']),
            transaction_amount= float(sample['transaction_amount'])
        )

        # ── Summary row ──
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Transaction ID", evidence.transaction_id)
        m2.metric("Amount", f"₹{evidence.transaction_amount:,.2f}")
        m3.metric("Reason Code", REASON_LABELS.get(evidence.reason_code, evidence.reason_code))
        m4.metric("Device Trust", f"{evidence.device_trust_score:.2f}")
        m5.metric("Customer Age", f"{evidence.customer_history_days}d")

        st.markdown("---")
        left, right = st.columns(2)

        # ── STAGE 1 ──
        with left:
            st.markdown('<div class="stage-badge">STAGE 1 · AI VERIFIER</div>', unsafe_allow_html=True)
            st.markdown("#### LightGBM Risk Score")

            if model:
                pred_row = sample[FEATURES].to_frame().T.copy()
                pred_row['reason_code'] = pred_row['reason_code'].astype(str).astype('category')
                prob = float(model.predict(pred_row)[0])
                is_def = prob > THRESHOLD

                # Probability gauge using progress bar
                st.markdown(f"**Win Probability: `{prob:.1%}`**")
                st.progress(min(prob, 1.0))
                st.caption(f"Cost-optimal threshold: {THRESHOLD:.3f} · "
                           f"{'✅ Above' if is_def else '❌ Below'} threshold")

                if is_def:
                    st.markdown(f"""
                    <div class="verdict-win">
                      <span>✅ DEFENSIBLE</span><br>
                      <small style="color:#a0d0b0">Win probability {prob:.1%} exceeds threshold {THRESHOLD:.1%}.
                      Escalating to Auto-Responder.</small>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="verdict-loss">
                      <span>❌ NOT DEFENSIBLE</span><br>
                      <small style="color:#d09090">Win probability {prob:.1%} is below threshold {THRESHOLD:.1%}.
                      Recommendation: Accept liability. Save dispute cost.</small>
                    </div>""", unsafe_allow_html=True)

            # Evidence log
            st.markdown("<br>**📋 Raw Evidence Log**", unsafe_allow_html=True)
            ev_items = {
                "AVS Match":           "✅ Yes" if evidence.avs_match else "❌ No",
                "CVV Match":           "✅ Yes" if evidence.cvv_match else "❌ No",
                "IP/Geo Match":        "✅ Yes" if evidence.ip_geo_match else "❌ No",
                "Delivery Confirmed":  "✅ Yes" if evidence.delivery_confirmed else "❌ No",
                "Is Digital Good":     "Yes" if evidence.is_digital_good else "No",
                "Prior Disputes":      str(evidence.prior_disputes),
            }
            ev_df = pd.DataFrame(ev_items.items(), columns=["Evidence Field", "Status"])
            st.dataframe(ev_df, use_container_width=True, hide_index=True)

        # ── STAGE 2 ──
        with right:
            st.markdown('<div class="stage-badge">STAGE 2 · AUTO-RESPONDER</div>', unsafe_allow_html=True)
            st.markdown("#### Grounded Defense Packet")

            with st.spinner("Orchestrator assembling grounded defense packet…"):
                packet = generate_defense_packet(evidence)

            # Defense packet display
            pkt_dict = packet.model_dump()

            st.markdown(f"**Defensible:** {'✅ Yes' if packet.is_defensible else '❌ No'}")
            st.markdown(f"**Evidence Category:** `{packet.compelling_evidence_category}`")
            st.markdown(f"**Template Selected:** `{packet.explanation_template_id}`")

            st.markdown("<br>**🔒 Guardrail Diagnostics**", unsafe_allow_html=True)
            pills = []
            checks = [
                ("Delivery Confirmed", packet.asserts_delivery_confirmed),
                ("Auth Match (AVS+CVV)", packet.asserts_auth_match),
                ("Device/IP Match", packet.asserts_device_match),
            ]
            for label, val in checks:
                if val is True:
                    pills.append(f'<span class="pill-ok">✅ {label}: Grounded</span>')
                else:
                    pills.append(f'<span class="pill-omit">⚪ {label}: Omitted</span>')
            st.markdown(" ".join(pills), unsafe_allow_html=True)

            st.markdown("<br>**📄 Raw JSON Payload**", unsafe_allow_html=True)
            st.json(pkt_dict)

            ground_truth = "🏆 WON" if int(sample['dispute_won']) == 1 else "❌ LOST"
            st.info(f"**Ground-Truth Label (test set):** {ground_truth}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EVALUATION DEEP-DIVE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Evaluation Deep-Dive":
    st.markdown("""
    <div class="hero">
      <h1>📊 Evaluation Deep-Dive</h1>
      <p>Full metrics on the strictly held-out 10,000-record test set · never touched during training or threshold tuning</p>
    </div>
    """, unsafe_allow_html=True)

    if df is None or model is None:
        st.error("Model or test data not found."); st.stop()

    FEATURES = [
        'transaction_amount','avs_match','cvv_match','device_trust_score',
        'ip_geo_match','delivery_confirmed','is_digital_good',
        'customer_history_days','prior_disputes','confounder_feature','reason_code'
    ]

    with st.spinner("Running full evaluation on held-out test set…"):
        X_test = df[FEATURES].copy()
        X_test['reason_code'] = X_test['reason_code'].astype(str).astype('category')
        y_test = df['dispute_won']
        preds_prob   = model.predict(X_test)
        preds_binary = (preds_prob > THRESHOLD).astype(int)

        pr_auc    = average_precision_score(y_test, preds_prob)
        precision = precision_score(y_test, preds_binary)
        recall    = recall_score(y_test, preds_binary)
        f1        = f1_score(y_test, preds_binary)

    # ── Global Metrics ──
    st.markdown("### 🎯 Global Metrics")
    g1, g2, g3, g4 = st.columns(4)
    for col, (lbl, val, sub) in zip(
        [g1, g2, g3, g4],
        [("PR-AUC", f"{pr_auc:.4f}", "Threshold-independent"),
         ("Precision", f"{precision:.4f}", f"@ threshold {THRESHOLD:.3f}"),
         ("Recall",    f"{recall:.4f}",    "Recall-biased by design"),
         ("F1 Score",  f"{f1:.4f}",        "Harmonic mean")]
    ):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{lbl}</div>
            <div class="value">{val}</div>
            <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    chart_l, chart_r = st.columns(2)

    # ── PR Curve ──
    with chart_l:
        st.markdown("#### Precision-Recall Curve")
        prec_curve, rec_curve, _ = precision_recall_curve(y_test, preds_prob)
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("#1a1d24")
        ax.set_facecolor("#1a1d24")
        ax.plot(rec_curve, prec_curve, color="#1a56ff", lw=2, label=f"PR-AUC = {pr_auc:.4f}")
        ax.axhline(y=precision, color="#00d26a", linestyle="--", lw=1.2, label=f"Precision @ threshold ({precision:.3f})")
        ax.axvline(x=recall,    color="#ffaa00", linestyle="--", lw=1.2, label=f"Recall @ threshold ({recall:.3f})")
        ax.set_xlabel("Recall", color="#a0b4ff")
        ax.set_ylabel("Precision", color="#a0b4ff")
        ax.tick_params(colors="#a0b4ff")
        ax.legend(fontsize=8, facecolor="#262730", labelcolor="white")
        for spine in ax.spines.values(): spine.set_edgecolor("#2a2d3a")
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Confusion Matrix (live) ──
    with chart_r:
        st.markdown("#### Confusion Matrix")
        cm = confusion_matrix(y_test, preds_binary)
        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#1a1d24")
        ax.set_facecolor("#1a1d24")
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["Pred: Drop", "Pred: Defend"],
                    yticklabels=["Actual: Loss", "Actual: Win"],
                    ax=ax, cbar=False,
                    annot_kws={"size": 14, "color": "white"})
        ax.tick_params(colors="#a0b4ff")
        ax.set_xlabel("Prediction", color="#a0b4ff")
        ax.set_ylabel("Ground Truth", color="#a0b4ff")
        ax.set_title(f"Threshold = {THRESHOLD:.3f}", color="#a0b4ff", fontsize=10)
        st.pyplot(fig, use_container_width=True)
        plt.close()

    # ── Cost curve ──
    st.markdown("#### Cost Optimisation Curve (Validation Set Logic Applied to Test)")
    FP_COST = 500
    thresholds = np.linspace(0.1, 0.9, 81)
    costs, fp_costs, fn_costs = [], [], []
    for t in thresholds:
        pb = (preds_prob > t).astype(int)
        fp_m = (pb == 1) & (y_test.values == 0)
        fn_m = (pb == 0) & (y_test.values == 1)
        fpc  = fp_m.sum() * FP_COST
        fnc  = (df.loc[fn_m, 'transaction_amount'].values + 1500).sum()
        costs.append(fpc + fnc)
        fp_costs.append(fpc)
        fn_costs.append(fnc)

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#1a1d24")
    ax.set_facecolor("#1a1d24")
    ax.fill_between(thresholds, fp_costs, alpha=0.25, color="#ffaa00", label="FP Cost (ops waste)")
    ax.fill_between(thresholds, fn_costs, alpha=0.25, color="#ff4444", label="FN Cost (revenue loss)")
    ax.plot(thresholds, costs, color="#1a56ff", lw=2.5, label="Total Expected Cost (₹)")
    ax.axvline(x=THRESHOLD, color="#00d26a", linestyle="--", lw=1.5,
               label=f"Optimal Threshold {THRESHOLD:.2f}")
    ax.scatter([THRESHOLD], [min(costs)], color="#00d26a", zorder=5, s=80)
    ax.set_xlabel("Decision Threshold", color="#a0b4ff")
    ax.set_ylabel("Total Cost (₹)", color="#a0b4ff")
    ax.tick_params(colors="#a0b4ff")
    ax.legend(facecolor="#262730", labelcolor="white", fontsize=9)
    for spine in ax.spines.values(): spine.set_edgecolor("#2a2d3a")
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.caption("FP Cost assumption: ₹500 (ops time + acquirer win-ratio risk). "
               "FN Cost assumption: transaction amount + ₹1,500 (typical Visa/MC chargeback fee). "
               "Both are stated assumptions, not Razorpay-sourced data.")

    # ── Per reason code table ──
    st.markdown("#### Per Reason Code Breakdown")
    rows = []
    for code in df['reason_code'].astype(str).unique():
        mask = df['reason_code'].astype(str) == code
        y_sub  = y_test[mask]
        pb_sub = preds_binary[mask]
        rows.append({
            "Reason Code": REASON_LABELS.get(code, code),
            "Test N": int(mask.sum()),
            "Precision": f"{precision_score(y_sub, pb_sub, zero_division=0):.3f}",
            "Recall":    f"{recall_score(y_sub,    pb_sub, zero_division=0):.3f}",
            "F1":        f"{f1_score(y_sub,         pb_sub, zero_division=0):.3f}",
            "Base Win Rate": f"{y_sub.mean():.1%}",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Feature importance ──
    st.markdown("#### LightGBM Feature Importance (Gain)")
    fi = pd.Series(
        model.feature_importance(importance_type="gain"),
        index=FEATURES
    ).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#1a1d24")
    ax.set_facecolor("#1a1d24")
    bars = ax.barh(fi.index, fi.values, color="#1a56ff", alpha=0.8)
    ax.tick_params(colors="#a0b4ff")
    ax.set_xlabel("Importance (Gain)", color="#a0b4ff")
    for spine in ax.spines.values(): spine.set_edgecolor("#2a2d3a")
    st.pyplot(fig, use_container_width=True)
    plt.close()
