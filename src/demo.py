import pandas as pd
import json
import os
from src.schemas import DisputeEvidence
from src.responder import generate_defense_packet

def run_demo():
    print("=== RazorSentinel-AI Demo ===")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    test_path = os.path.join(data_dir, "test_set.csv")
    
    if not os.path.exists(test_path):
        print("Test set not found. Please run data generator and training scripts first.")
        return
        
    df = pd.read_csv(test_path)
    # Pick a defensible record
    sample = df[df['dispute_won'] == 1].iloc[0]
    
    evidence = DisputeEvidence(
        transaction_id=sample['transaction_id'],
        reason_code=str(sample['reason_code']),
        avs_match=bool(sample['avs_match']),
        cvv_match=bool(sample['cvv_match']),
        device_trust_score=float(sample['device_trust_score']),
        ip_geo_match=bool(sample['ip_geo_match']),
        delivery_confirmed=bool(sample['delivery_confirmed']),
        is_digital_good=bool(sample['is_digital_good']),
        customer_history_days=int(sample['customer_history_days']),
        prior_disputes=int(sample['prior_disputes']),
        transaction_amount=float(sample['transaction_amount'])
    )
    
    print("\n[Input] Extracted Evidence:")
    print(evidence.model_dump_json(indent=2))
    
    print("\n[Processing] Orchestrator assembling defense packet...")
    packet = generate_defense_packet(evidence)
    
    print("\n[Output] Final Verified Defense Packet:")
    print(packet.model_dump_json(indent=2))

if __name__ == "__main__":
    run_demo()
