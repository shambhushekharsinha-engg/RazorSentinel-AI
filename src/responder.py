import os
import json
from google import genai
from src.schemas import DisputeEvidence, DefensePacket

def generate_defense_packet(evidence: DisputeEvidence) -> DefensePacket:
    """
    Takes structured dispute evidence and uses an LLM to select the appropriate
    defense strategy and evidence claims.
    
    Includes a strict post-generation grounding check (Refinement 3) to ensure
    the LLM cannot hallucinate claims that contradict the source evidence.
    """
    
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("WARNING: No API key set (GEMINI_API_KEY or GOOGLE_API_KEY). Using deterministic fallback.")
        return deterministic_fallback(evidence)

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an automated chargeback defense orchestrator.
    Review the following structured evidence for a dispute:
    {evidence.model_dump_json(indent=2)}
    
    Determine if this dispute is defensible and strictly select the evidence flags.
    DO NOT assert any flags to be true unless the evidence explicitly supports them.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': DefensePacket,
                'temperature': 0.0
            },
        )
        # Assuming google-genai SDK maps this to a dict or Pydantic model
        packet_dict = json.loads(response.text)
        packet = DefensePacket(**packet_dict)
    except Exception as e:
        print(f"LLM Generation failed: {e}. Falling back to deterministic.")
        packet = deterministic_fallback(evidence)

    # ---------------------------------------------------------
    # Refinement 3: Anti-Hallucination Strict Grounding Check
    # ---------------------------------------------------------
    # Even if the LLM hallucinates an assertion, we strictly prune it
    # against the exact source evidence dictionary by omitting it (None)
    # rather than asserting it is false.
    
    if packet.asserts_delivery_confirmed and not evidence.delivery_confirmed:
        print("[GUARDRAIL] Dropped hallucinated delivery claim (set to None).")
        packet.asserts_delivery_confirmed = None
        
    if packet.asserts_auth_match and not (evidence.avs_match and evidence.cvv_match):
        print("[GUARDRAIL] Dropped hallucinated auth match claim (set to None).")
        packet.asserts_auth_match = None
        
    if packet.asserts_device_match and not (evidence.ip_geo_match and evidence.device_trust_score > 0.7):
        print("[GUARDRAIL] Dropped hallucinated device match claim (set to None).")
        packet.asserts_device_match = None

    return packet

def deterministic_fallback(evidence: DisputeEvidence) -> DefensePacket:
    is_defensible = (
        (evidence.delivery_confirmed and not evidence.is_digital_good) or
        (evidence.avs_match and evidence.cvv_match and evidence.ip_geo_match) or
        (evidence.device_trust_score > 0.8)
    )
    
    tpl = "TPL_WEAK"
    category = "None"
    if evidence.delivery_confirmed:
        tpl = "TPL_DELIVERY"
        category = "Proof of Delivery"
    elif evidence.avs_match and evidence.cvv_match:
        tpl = "TPL_AUTH"
        category = "Device/IP Linkage"
        
    return DefensePacket(
        is_defensible=bool(is_defensible),
        compelling_evidence_category=category,
        asserts_delivery_confirmed=bool(evidence.delivery_confirmed) if evidence.delivery_confirmed else None,
        asserts_device_match=bool(evidence.ip_geo_match and evidence.device_trust_score > 0.7) if (evidence.ip_geo_match and evidence.device_trust_score > 0.7) else None,
        asserts_auth_match=bool(evidence.avs_match and evidence.cvv_match) if (evidence.avs_match and evidence.cvv_match) else None,
        explanation_template_id=tpl
    )
