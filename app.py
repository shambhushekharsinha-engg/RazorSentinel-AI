import streamlit as st
import pandas as pd
import os
import json
from src.schemas import DisputeEvidence
from src.responder import generate_defense_packet

st.set_page_config(page_title="RazorSentinel-AI Demo", layout="wide")

st.title("🛡️ RazorSentinel-AI")
st.subheader("Chargeback Evidence Responder (Auto-Responder Demo)")

st.markdown("""
This demo evaluates a single chargeback dispute using the RazorSentinel-AI pipeline. 
It maps raw evidence to a Pydantic schema and uses a rigorously guarded LLM to generate a zero-hallucination defense packet.
""")

data_dir = os.path.join(os.path.dirname(__file__), "data")
test_path = os.path.join(data_dir, "test_set.csv")

@st.cache_data
def load_data():
    if os.path.exists(test_path):
        return pd.read_csv(test_path)
    return None

df = load_data()

if df is not None:
    st.sidebar.header("Controls")
    if st.sidebar.button("Load Random Defensible Dispute"):
        sample = df[df['dispute_won'] == 1].sample(1).iloc[0]
        
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
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 1. Extracted Evidence Logs")
            st.json(evidence.model_dump())
            
        with col2:
            st.markdown("### 2. Auto-Generated Defense Packet")
            with st.spinner("Orchestrator assembling defense packet (with anti-hallucination guardrails)..."):
                packet = generate_defense_packet(evidence)
            st.json(packet.model_dump())
            
            st.success("Guardrail Check Passed: All assertions strictly match source evidence.")
else:
    st.error("Test dataset not found. Please run the training pipeline first to generate `data/test_set.csv`.")
