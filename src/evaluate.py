import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    test_path = os.path.join(data_dir, "test_set.csv")
    model_path = os.path.join(data_dir, "verifier_model.pkl")
    threshold_path = os.path.join(data_dir, "optimal_threshold.txt")
    
    df = pd.read_csv(test_path)
    df['reason_code'] = df['reason_code'].astype(str).astype('category')
    model = joblib.load(model_path)
    
    with open(threshold_path, "r") as f:
        best_threshold = float(f.read().strip())
        
    features = [
        'transaction_amount', 'avs_match', 'cvv_match', 
        'device_trust_score', 'ip_geo_match', 'delivery_confirmed', 
        'is_digital_good', 'customer_history_days', 'prior_disputes',
        'confounder_feature', 'reason_code'
    ]
    
    X_test = df[features]
    y_test = df['dispute_won']
    
    # Refinement 4: Assert minimum test-set volume per reason code
    reason_code_counts = X_test['reason_code'].value_counts()
    for code, count in reason_code_counts.items():
        assert count > 100, f"Insufficient test-set volume for reason code {code}: {count} samples."
        
    # Predict probabilities
    preds_prob = model.predict(X_test)
    preds_binary = (preds_prob > best_threshold).astype(int)
    
    # Refinement 5: Report default PR-AUC and cost-optimal threshold PR
    pr_auc = average_precision_score(y_test, preds_prob)
    precision = precision_score(y_test, preds_binary)
    recall = recall_score(y_test, preds_binary)
    f1 = f1_score(y_test, preds_binary)
    
    print("=== GLOBAL METRICS (HELD-OUT TEST SET) ===")
    print(f"PR-AUC (Threshold Independent): {pr_auc:.4f}")
    print(f"Optimal Threshold Used: {best_threshold:.3f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("=========================================\n")
    
    print("=== PER REASON CODE METRICS ===")
    for code in X_test['reason_code'].unique():
        mask = X_test['reason_code'] == code
        y_test_sub = y_test[mask]
        preds_binary_sub = preds_binary[mask]
        
        p = precision_score(y_test_sub, preds_binary_sub, zero_division=0)
        r = recall_score(y_test_sub, preds_binary_sub, zero_division=0)
        count = mask.sum()
        print(f"Code {code} (N={count}): Precision={p:.3f}, Recall={r:.3f}")
        
    # Cost Curve Generation
    FP_COST = 500
    def fn_cost(amount):
        return amount + 1500
        
    thresholds = np.linspace(0.1, 0.9, 81)
    costs = []
    
    for t in thresholds:
        pb = (preds_prob > t).astype(int)
        fp_mask = (pb == 1) & (y_test.values == 0)
        fn_mask = (pb == 0) & (y_test.values == 1)
        
        fp_c = fp_mask.sum() * FP_COST
        fn_c = fn_cost(df.loc[fn_mask, 'transaction_amount'].values).sum()
        costs.append(fp_c + fn_c)
        
    plt.figure(figsize=(10, 5))
    plt.plot(thresholds, costs, label='Total Expected Cost (₹)', color='red')
    plt.axvline(x=best_threshold, color='blue', linestyle='--', label=f'Optimal Threshold ({best_threshold:.2f})')
    plt.title('Cost Optimization Curve (Test Set)')
    plt.xlabel('Decision Threshold')
    plt.ylabel('Total Cost (FP + FN)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(data_dir, "cost_curve.png"))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, preds_binary)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Pred Loss (Drop)', 'Pred Win (Defend)'],
                yticklabels=['Actual Loss', 'Actual Win'])
    plt.title(f'Confusion Matrix @ Threshold {best_threshold:.2f}')
    plt.ylabel('Ground Truth')
    plt.xlabel('Prediction')
    plt.savefig(os.path.join(data_dir, "confusion_matrix.png"))
    
    print("\nVisualizations saved: cost_curve.png, confusion_matrix.png")

if __name__ == "__main__":
    evaluate()
