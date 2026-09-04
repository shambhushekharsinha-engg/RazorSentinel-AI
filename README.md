# RazorSentinel-AI

**Track:** Razorpay AI Buildathon — Track 02: AI Risk Manager

RazorSentinel-AI is a two-stage Chargeback Evidence Responder focused exclusively on a single class of loss: **Chargebacks and Disputes**. 

Instead of an unconstrained AI tool, this project enforces strict mathematical bounds on operational costs and structural guardrails against AI hallucinations, making it 100% defense-only.

## 1. The Architecture (Verifier + Auto-Responder)

The system works in two stages:
1. **Verifier:** A LightGBM classifier scores structured dispute evidence to predict if the dispute is defensible (win/loss). 
2. **Auto-Responder:** If defensible, an LLM assembles a structured defense packet. A rigid post-generation validation layer ensures every claim selected by the LLM is perfectly grounded in the source logs, guaranteeing zero hallucination.

## 2. Honest Metrics & Cost-Weighted Thresholding

We explicitly model the cost of decisions:
* **False Positive (FP) Cost:** ₹500. This assumes the wasted operational time to file a weak dispute, plus the hidden penalty of hurting the merchant's win-ratio with the acquirer.
* **False Negative (FN) Cost:** Transaction Amount + ₹1500. This is the direct revenue lost plus typical assumed Visa/Mastercard dispute fees.

Rather than maximizing raw accuracy, the Verifier finds the mathematically optimal decision threshold on a validation set to minimize this total expected cost.

## 3. Evaluation on Held-Out Test Set (50k Synthetic Records)

*Note: The dataset was synthesized purely for evaluating defense logic, not for generating fraudulent attack patterns. To prevent the model from learning a trivial mapping, we explicitly injected a 12% random label-flip noise factor along with confounder features. The resulting 0.75 PR-AUC represents strong, non-trivial learning over this noisy baseline.*

The system is evaluated on a strictly held-out test split. The evaluation script reports:
- **PR-AUC** (Threshold Independent)
- **Precision, Recall, and F1** (at the cost-optimal threshold). *Note: The optimal threshold (0.29) intentionally heavily favors Recall (90%) over Precision (62%) because the direct financial loss of missing a winnable dispute (False Negative) mathematically outweighs the operational cost of filing a weak one (False Positive).*
- **Per-Reason Code Metrics** (breaking down performance across 10.4, 13.1, 4853, etc.)

Check the `data/cost_curve.png` and `data/confusion_matrix.png` for visualizations of the cost-optimization logic.

## 4. Defense-Only Guarantee

The `responder.py` utilizes a "structured-in / structured-out" schema constraint (via Pydantic). The LLM cannot write free-form prose to defend a dispute; it must toggle explicit Boolean evidence flags. 
Furthermore, a strict python guardrail drops any flag if the source evidence does not 100% support it, ensuring the auto-responder cannot fabricate a persuasive-but-false claim.
