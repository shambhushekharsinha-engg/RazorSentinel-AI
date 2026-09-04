from pydantic import BaseModel, Field
from typing import Literal, Optional

class DisputeEvidence(BaseModel):
    transaction_id: str
    reason_code: str
    avs_match: bool
    cvv_match: bool
    device_trust_score: float
    ip_geo_match: bool
    delivery_confirmed: bool
    is_digital_good: bool
    customer_history_days: int
    prior_disputes: int
    transaction_amount: float

class DefensePacket(BaseModel):
    is_defensible: bool = Field(
        description="Based on the evidence, is this dispute defensible?"
    )
    compelling_evidence_category: Literal["Proof of Delivery", "Device/IP Linkage", "Prior Legitimate History", "None"] = Field(
        description="The primary category of evidence to be submitted."
    )
    # Refinement: Structured-in/structured-out. Instead of free-text claims, 
    # the LLM asserts specific boolean flags that map directly to the evidence dict.
    # Optional[bool] allows us to omit claims (None) rather than falsely asserting False.
    asserts_delivery_confirmed: Optional[bool] = Field(
        default=None,
        description="Set to true ONLY if the provided evidence explicitly states delivery_confirmed is true."
    )
    asserts_device_match: Optional[bool] = Field(
        default=None,
        description="Set to true ONLY if the provided evidence explicitly states ip_geo_match is true and device_trust_score is high."
    )
    asserts_auth_match: Optional[bool] = Field(
        default=None,
        description="Set to true ONLY if the provided evidence explicitly states avs_match and cvv_match are true."
    )
    explanation_template_id: Literal["TPL_DELIVERY", "TPL_AUTH", "TPL_HISTORY", "TPL_WEAK"] = Field(
        description="Select a standard standard boilerplate explanation template ID based on the strongest evidence category."
    )
