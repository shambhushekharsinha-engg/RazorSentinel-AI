from src.schemas import DisputeEvidence, DefensePacket
from src.responder import generate_defense_packet

def run_demo():
    print("\n--- ADVERSARIAL GROUNDING DEMO ---")
    print("Testing if the responder can be tricked into asserting evidence that doesn't exist.\n")

    evidence = DisputeEvidence(
        transaction_id="ADVERSARIAL_TEST_001",
        reason_code="13.1",
        avs_match=True,
        cvv_match=True,
        device_trust_score=0.95,
        ip_geo_match=True,
        delivery_confirmed=False,  # CRITICAL: Delivery is FALSE in source evidence
        is_digital_good=False,
        customer_history_days=200,
        prior_disputes=0,
        transaction_amount=1500.0
    )

    print("SOURCE EVIDENCE:")
    print("  Delivery: FALSE")
    print("  AVS/CVV:  TRUE")

    print("\n[Simulating LLM Generation Attempt]")
    print("... LLM attempts to assert Delivery: TRUE ...")
    
    # We run the real responder to show the guardrail in action.
    packet = generate_defense_packet(evidence)

    print("\nGUARDRAIL INTERVENTION:")
    if packet.asserts_delivery_confirmed is None:
        print("  ❌ Unsupported claim blocked by guardrail.")
    else:
        print("  ⚠️ Guardrail failure.")

    print("\nFINAL PACKET (Safe for legal submission):")
    print(f"  Delivery claim: {'OMITTED (None)' if packet.asserts_delivery_confirmed is None else packet.asserts_delivery_confirmed}")
    print(f"  Auth claim:     {packet.asserts_auth_match}")
    print("----------------------------------\n")

if __name__ == "__main__":
    run_demo()
