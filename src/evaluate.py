"""
src/evaluate.py
===============
Held-out test set evaluation for RazorSentinel-AI.

Produces:
  - Console report of global and per-reason-code metrics
  - data/metrics.json  (structured metrics artifact, loaded by CI and dashboard)
  - data/cost_curve.png
  - data/confusion_matrix.png

All metrics are computed on the strictly held-out test set (20% of 50k records).
This file must NEVER be used to select or tune the threshold — that happens in train_verifier.py.
"""

import json
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    average_precision_score, confusion_matrix,
)
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    test_path      = os.path.join(data_dir, "test_set.csv")
    model_path     = os.path.join(data_dir, "verifier_model.pkl")
    threshold_path = os.path.join(data_dir, "optimal_threshold.txt")

    df = pd.read_csv(test_path)
    df["reason_code"] = df["reason_code"].astype(str).astype("category")
    model = joblib.load(model_path)

    with open(threshold_path, "r") as f:
        best_threshold = float(f.read().strip())

    features = [
        "transaction_amount", "avs_match", "cvv_match",
        "device_trust_score", "ip_geo_match", "delivery_confirmed",
        "is_digital_good", "customer_history_days", "prior_disputes",
        "confounder_feature", "reason_code",
    ]

    X_test = df[features]
    y_test = df["dispute_won"]

    # ── Assert minimum test-set volume per reason code ────────────────────────
    reason_code_counts = X_test["reason_code"].value_counts()
    for code, count in reason_code_counts.items():
        assert count > 100, (
            f"Insufficient test-set volume for reason code {code}: {count} samples."
        )

    # ── Predict ───────────────────────────────────────────────────────────────
    preds_prob   = model.predict(X_test)
    preds_binary = (preds_prob > best_threshold).astype(int)

    # ── Global Metrics ────────────────────────────────────────────────────────
    pr_auc    = average_precision_score(y_test, preds_prob)
    precision = precision_score(y_test, preds_binary)
    recall    = recall_score(y_test, preds_binary)
    f1        = f1_score(y_test, preds_binary)

    print("=== GLOBAL METRICS (HELD-OUT TEST SET) ===")
    print(f"PR-AUC (Threshold Independent): {pr_auc:.4f}")
    print(f"Optimal Threshold Used:         {best_threshold:.3f}")
    print(f"Precision:                      {precision:.4f}")
    print(f"Recall:                         {recall:.4f}")
    print(f"F1 Score:                       {f1:.4f}")
    print("=" * 43 + "\n")

    # ── Threshold Sensitivity Table ───────────────────────────────────────────
    print("=== THRESHOLD SENSITIVITY ===")
    sensitivity_rows = []
    for t in [0.20, 0.25, 0.29, 0.35, 0.40, 0.50]:
        pb = (preds_prob > t).astype(int)
        p_ = precision_score(y_test, pb, zero_division=0)
        r_ = recall_score(y_test, pb, zero_division=0)
        f_ = f1_score(y_test, pb, zero_division=0)
        marker = " ← OPTIMAL" if abs(t - best_threshold) < 0.001 else ""
        print(f"  t={t:.2f}  P={p_:.3f}  R={r_:.3f}  F1={f_:.3f}{marker}")
        sensitivity_rows.append({"threshold": t, "precision": round(p_, 4),
                                  "recall": round(r_, 4), "f1": round(f_, 4)})
    print()

    # ── Per Reason Code Metrics ───────────────────────────────────────────────
    print("=== PER REASON CODE METRICS ===")
    per_code_metrics = {}
    for code in X_test["reason_code"].unique():
        mask = X_test["reason_code"] == code
        y_sub = y_test[mask]
        pb_sub = preds_binary[mask]
        p_ = precision_score(y_sub, pb_sub, zero_division=0)
        r_ = recall_score(y_sub, pb_sub, zero_division=0)
        f_ = f1_score(y_sub, pb_sub, zero_division=0)
        count = int(mask.sum())
        win_rate = float(y_sub.mean())
        print(f"  Code {code} (N={count:>5}): P={p_:.3f}  R={r_:.3f}  F1={f_:.3f}  WinRate={win_rate:.1%}")
        per_code_metrics[str(code)] = {
            "n": count, "win_rate": round(win_rate, 4),
            "precision": round(p_, 4), "recall": round(r_, 4), "f1": round(f_, 4),
        }
    print()

    # ── Per Transaction Amount Bucket ─────────────────────────────────────────
    print("=== PER AMOUNT BUCKET METRICS ===")
    amount_buckets = [
        ("< ₹500",    df["transaction_amount"] < 500),
        ("₹500–2K",  (df["transaction_amount"] >= 500)  & (df["transaction_amount"] < 2000)),
        ("₹2K–5K",   (df["transaction_amount"] >= 2000) & (df["transaction_amount"] < 5000)),
        ("> ₹5K",    df["transaction_amount"] >= 5000),
    ]
    per_amount_metrics = {}
    for label, mask in amount_buckets:
        y_sub  = y_test[mask]
        pb_sub = preds_binary[mask]
        if len(y_sub) == 0:
            continue
        p_ = precision_score(y_sub, pb_sub, zero_division=0)
        r_ = recall_score(y_sub, pb_sub, zero_division=0)
        f_ = f1_score(y_sub, pb_sub, zero_division=0)
        count = int(mask.sum())
        print(f"  {label:<10} (N={count:>5}): P={p_:.3f}  R={r_:.3f}  F1={f_:.3f}")
        per_amount_metrics[label] = {
            "n": count, "precision": round(p_, 4),
            "recall": round(r_, 4), "f1": round(f_, 4),
        }
    print()

    # ── Save metrics.json ─────────────────────────────────────────────────────
    metrics = {
        "global": {
            "pr_auc":         round(pr_auc, 4),
            "threshold":      round(best_threshold, 3),
            "precision":      round(precision, 4),
            "recall":         round(recall, 4),
            "f1":             round(f1, 4),
            "test_set_size":  int(len(y_test)),
            "positive_rate":  round(float(y_test.mean()), 4),
        },
        "per_reason_code":  per_code_metrics,
        "per_amount_bucket": per_amount_metrics,
        "threshold_sensitivity": sensitivity_rows,
        "cost_model": {
            "fp_cost_inr":    500,
            "fn_base_fee_inr": 1500,
            "note": "Stated assumptions — not Razorpay-sourced data.",
        },
    }
    metrics_path = os.path.join(data_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"metrics.json saved → {metrics_path}")

    # ── Cost Curve ────────────────────────────────────────────────────────────
    FP_COST = 500
    thresholds = np.linspace(0.1, 0.9, 81)
    costs, fp_costs, fn_costs = [], [], []

    for t in thresholds:
        pb = (preds_prob > t).astype(int)
        fp_mask = (pb == 1) & (y_test.values == 0)
        fn_mask = (pb == 0) & (y_test.values == 1)
        fpc = fp_mask.sum() * FP_COST
        fnc = (df.loc[fn_mask, "transaction_amount"].values + 1500).sum()
        costs.append(fpc + fnc)
        fp_costs.append(fpc)
        fn_costs.append(fnc)

    plt.figure(figsize=(10, 5))
    plt.fill_between(thresholds, fp_costs, alpha=0.15, color="orange", label="FP Cost")
    plt.fill_between(thresholds, fn_costs, alpha=0.15, color="red",    label="FN Cost")
    plt.plot(thresholds, costs, label="Total Expected Cost (₹)", color="steelblue", linewidth=2)
    plt.axvline(x=best_threshold, color="green", linestyle="--",
                label=f"Optimal @ {best_threshold:.2f}")
    plt.title("Cost Optimisation Curve (Test Set)")
    plt.xlabel("Decision Threshold")
    plt.ylabel("Total Cost (FP + FN) — ₹")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "cost_curve.png"), dpi=120)
    plt.close()

    # ── Confusion Matrix ──────────────────────────────────────────────────────
    cm = confusion_matrix(y_test, preds_binary)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Pred: Drop", "Pred: Defend"],
                yticklabels=["Actual: Lost", "Actual: Won"])
    plt.title(f"Confusion Matrix @ Threshold {best_threshold:.3f}")
    plt.ylabel("Ground Truth")
    plt.xlabel("Prediction")
    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, "confusion_matrix.png"), dpi=120)
    plt.close()

    print("\nVisualizations saved: cost_curve.png, confusion_matrix.png")


if __name__ == "__main__":
    evaluate()
