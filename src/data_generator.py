import pandas as pd
import numpy as np
import random
import os

# Visa/MC Reason Codes Mapping
# 10.4: Fraud - Card Absent Environment
# 13.1: Merchandise/Services Not Received
# 13.3: Not as Described or Defective Merchandise
# 11.1: Card Recovery Bulletin
# 4853: Cardholder Dispute (Mastercard general)
REASON_CODES = ["10.4", "13.1", "13.3", "11.1", "4853"]

def generate_data(num_records=50000, output_path="../data/synthetic_disputes.csv"):
    """
    Generates synthetic evaluation data for the Chargeback Evidence Responder.
    This is purely for evaluation data synthesis, not an attack simulator.
    """
    np.random.seed(42)
    random.seed(42)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Generating {num_records} synthetic dispute records...")
    
    reason_codes = np.random.choice(REASON_CODES, size=num_records, p=[0.3, 0.3, 0.2, 0.05, 0.15])
    avs_match = np.random.choice([True, False], size=num_records, p=[0.8, 0.2])
    cvv_match = np.random.choice([True, False], size=num_records, p=[0.85, 0.15])
    device_trust_score = np.random.uniform(0.0, 1.0, size=num_records)
    ip_geo_match = np.random.choice([True, False], size=num_records, p=[0.75, 0.25])
    delivery_confirmed = np.random.choice([True, False], size=num_records, p=[0.6, 0.4])
    is_digital_good = np.random.choice([True, False], size=num_records, p=[0.4, 0.6])
    customer_history_days = np.random.randint(0, 1000, size=num_records)
    prior_disputes = np.random.poisson(0.1, size=num_records)
    
    # Confounder feature (Refinement 1): pure noise that a model might try to overfit if not careful
    confounder_feature = np.random.normal(50, 15, size=num_records)
    transaction_amounts = np.random.exponential(150, size=num_records).clip(5, 5000)
    
    # Base logic for dispute win probability
    win_scores = np.zeros(num_records)
    
    # Positive factors for winning a dispute
    win_scores += np.where(avs_match & cvv_match, 0.3, -0.2)
    win_scores += np.where(ip_geo_match, 0.1, -0.2)
    win_scores += (device_trust_score - 0.5) * 0.4  # scales from -0.2 to +0.2
    
    # Delivery confirmed is strong proof for 'Not Received' (13.1)
    win_scores += np.where((reason_codes == "13.1") & delivery_confirmed & ~is_digital_good, 0.6, 0)
    win_scores += np.where((reason_codes == "13.1") & ~delivery_confirmed & ~is_digital_good, -0.8, 0)
    
    # Fraud reasons (10.4) are hard to win without strong trust & auth
    win_scores += np.where((reason_codes == "10.4") & (device_trust_score < 0.4), -0.6, 0)
    win_scores += np.where((reason_codes == "10.4") & avs_match & cvv_match & ip_geo_match, 0.4, 0)
    
    # Prior disputes hurt merchant credibility
    win_scores -= (prior_disputes * 0.15)
    
    # Add gaussian noise to the scores to ensure noisy correlation
    win_scores += np.random.normal(0, 0.3, size=num_records)
    
    # Initial deterministic-ish labels based on threshold
    labels = win_scores > 0.1
    
    # Explicit Label Noise (Refinement 1): flip ~12% of labels to prevent trivial 99% accuracy
    flip_mask = np.random.rand(num_records) < 0.12
    labels = np.where(flip_mask, ~labels, labels)
    
    df = pd.DataFrame({
        'transaction_id': [f"txn_{i:06d}" for i in range(num_records)],
        'reason_code': reason_codes,
        'transaction_amount': np.round(transaction_amounts, 2),
        'avs_match': avs_match,
        'cvv_match': cvv_match,
        'device_trust_score': np.round(device_trust_score, 3),
        'ip_geo_match': ip_geo_match,
        'delivery_confirmed': delivery_confirmed,
        'is_digital_good': is_digital_good,
        'customer_history_days': customer_history_days,
        'prior_disputes': prior_disputes,
        'confounder_feature': np.round(confounder_feature, 3),
        'dispute_won': labels.astype(int)
    })
    
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    
    # Print basic stats
    win_rate = df['dispute_won'].mean()
    print(f"Overall Dispute Win Rate: {win_rate:.2%}")
    for code in REASON_CODES:
        code_win_rate = df[df['reason_code'] == code]['dispute_won'].mean()
        print(f"Win Rate for {code}: {code_win_rate:.2%}")

if __name__ == "__main__":
    # Ensure run from src/ directory or adjust path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    generate_data(output_path=os.path.join(data_dir, "synthetic_disputes.csv"))
