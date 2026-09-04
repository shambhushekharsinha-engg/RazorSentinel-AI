import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import joblib
import os

def train():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_disputes.csv")
    df = pd.read_csv(data_path)
    
    # 1. Feature Engineering & Selection
    features = [
        'transaction_amount', 'avs_match', 'cvv_match', 
        'device_trust_score', 'ip_geo_match', 'delivery_confirmed', 
        'is_digital_good', 'customer_history_days', 'prior_disputes',
        'confounder_feature' # Included to prove model doesn't just overfit
    ]
    
    # Encode categorical reason_code
    df['reason_code'] = df['reason_code'].astype('category')
    features.append('reason_code')
    
    X = df[features]
    y = df['dispute_won']
    
    # 2. Strict Train/Val/Test Split (60/20/20)
    # The test set is completely held out for evaluate.py
    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42, stratify=y_train_val)
    
    # Save the test set for the evaluation script
    test_df = X_test.copy()
    test_df['dispute_won'] = y_test
    # Also need transaction_id for responder mock if needed
    test_df['transaction_id'] = df.loc[X_test.index, 'transaction_id']
    test_df.to_csv(os.path.join(os.path.dirname(__file__), "..", "data", "test_set.csv"), index=False)
    
    print(f"Training on {len(X_train)} records, validating on {len(X_val)}, holding out {len(X_test)}.")
    
    # 3. Train LightGBM Verifier
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    
    params = {
        'objective': 'binary',
        'metric': 'auc', # auc for early stopping
        'learning_rate': 0.05,
        'num_leaves': 31,
        'verbose': -1
    }
    
    model = lgb.train(
        params,
        train_data,
        valid_sets=[val_data],
        num_boost_round=500,
        callbacks=[lgb.early_stopping(stopping_rounds=50)]
    )
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), "..", "data", "verifier_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # 4. Find Cost-Optimal Threshold on Validation Set
    val_preds = model.predict(X_val)
    
    # Cost Assumptions (Refinement 2)
    # FP Cost (Predicted Win, but actually Loss): Wasted ops time + risk to win-ratio (~₹500)
    FP_COST = 500
    
    # FN Cost (Predicted Loss, but actually Win): We drop the dispute and lose the revenue + bank fee (~₹1500)
    def fn_cost(amount):
        return amount + 1500
    
    val_amounts = X_val['transaction_amount'].values
    best_threshold = 0.5
    min_cost = float('inf')
    
    thresholds = np.linspace(0.1, 0.9, 81)
    for t in thresholds:
        preds_binary = (val_preds > t).astype(int)
        
        # False Positives: predicted 1, actual 0
        fp_mask = (preds_binary == 1) & (y_val.values == 0)
        total_fp_cost = fp_mask.sum() * FP_COST
        
        # False Negatives: predicted 0, actual 1
        fn_mask = (preds_binary == 0) & (y_val.values == 1)
        total_fn_cost = fn_cost(val_amounts[fn_mask]).sum()
        
        total_cost = total_fp_cost + total_fn_cost
        if total_cost < min_cost:
            min_cost = total_cost
            best_threshold = t
            
    print(f"Optimal Decision Threshold (Validation): {best_threshold:.3f}")
    
    # Save threshold for evaluation script
    with open(os.path.join(os.path.dirname(__file__), "..", "data", "optimal_threshold.txt"), "w") as f:
        f.write(str(best_threshold))

if __name__ == "__main__":
    train()
