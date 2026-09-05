import pytest
from src.schemas import DisputeEvidence, DefensePacket
from src.responder import generate_defense_packet
import os

def test_guardrail_removes_unsupported_delivery_claim():
    """
    Simulates a scenario where evidence does NOT support delivery, 
    but the system attempts to process it. Ensures guardrail forces 
    unsupported assertions to None.
    """
    evidence = DisputeEvidence(
        transaction_id="TXN_TEST_1",
        reason_code="13.1",
        avs_match=True,
        cvv_match=True,
        device_trust_score=0.9,
        ip_geo_match=True,
        delivery_confirmed=False, # FALSE in source truth
        is_digital_good=False,
        customer_history_days=100,
        prior_disputes=0,
        transaction_amount=5000.0
    )
    
    # We temporarily mock the Gemini call or rely on the deterministic fallback
    # To test the guardrail purely, we can bypass the LLM and pass a malformed packet
    # into the validation logic, or just run the full responder which triggers fallback if no key.
    
    # Let's ensure deterministic fallback doesn't hallucinate either.
    original_key = os.environ.get("GEMINI_API_KEY")
    if original_key:
        del os.environ["GEMINI_API_KEY"]
        
    packet = generate_defense_packet(evidence)
    
    # The guardrail MUST strip out asserts_delivery_confirmed if it was True,
    # or the fallback logic should correctly assess it.
    assert packet.asserts_delivery_confirmed is None or packet.asserts_delivery_confirmed is False, \
        "Guardrail failed to prevent an unsupported delivery claim."
        
    if original_key:
        os.environ["GEMINI_API_KEY"] = original_key

def test_guardrail_removes_unsupported_auth_claim():
    evidence = DisputeEvidence(
        transaction_id="TXN_TEST_2",
        reason_code="10.4",
        avs_match=False, # FALSE in source truth
        cvv_match=True,
        device_trust_score=0.9,
        ip_geo_match=True,
        delivery_confirmed=True,
        is_digital_good=False,
        customer_history_days=100,
        prior_disputes=0,
        transaction_amount=5000.0
    )
    
    packet = generate_defense_packet(evidence)
    assert packet.asserts_auth_match is None or packet.asserts_auth_match is False
