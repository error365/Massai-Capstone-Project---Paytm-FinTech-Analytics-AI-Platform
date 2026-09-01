import json
import os
from typing import Any, Dict

# Import disclosure snippets from project source file
from disclosure_snippets import DISCLOSURE_SNIPPETS  #[cite: 1]


def extract_signals(snippet: str) -> Dict[str, Any]:
  """Extracts structured risk, hedging, and sentiment metrics from disclosure text.

  Gated by MOCK_LLM environment variable (default: Mock mode enabled).
  """
  mock_mode = os.getenv("MOCK_LLM", "1") == "1"

  if mock_mode:
    snippet_lower = snippet.lower()

    # 1. Rule-Based Risk Flags Extraction
    risk_flags = []
    if "litigation" in snippet_lower:
      risk_flags.append("litigation")
    if "regulatory" in snippet_lower or "regulator" in snippet_lower:
      risk_flags.append("regulatory")
    if (
        "top three customers" in snippet_lower
        or "percent of total revenue" in snippet_lower
        or "concentration" in snippet_lower
    ):
      risk_flags.append("customer concentration")

    # 2. Rule-Based Hedging Phrase Detection
    hedging_keywords = ["assuming", "cautiously", "visibility"]
    hedging_detected = any(kw in snippet_lower for kw in hedging_keywords)

    # 3. Rule-Based Sentiment Classification
    if "confident" in snippet_lower or "approved" in snippet_lower:
      sentiment = "confident"
    elif hedging_detected:
      sentiment = "cautious"
    else:
      sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment,
    }

  else:
    # Optional Live LLM API Path with JSON Schema Validation & Retry
    # Add your preferred LLM provider call here (e.g. OpenAI/Gemini/Anthropic)
    pass


if __name__ == "__main__":
  print("=== Processing Corporate Disclosure Snippets ===")
  all_extractions = []

  for snippet in DISCLOSURE_SNIPPETS:  #[cite: 1]
    doc_id = snippet.split(":")[0]
    extracted_data = extract_signals(snippet)
    payload = {"doc_id": doc_id, **extracted_data}
    all_extractions.append(payload)

    print(
        f"[{doc_id}] Sentiment: {extracted_data['sentiment']} | Hedging:"
        f" {extracted_data['hedging_detected']} | Risks:"
        f" {extracted_data['risk_flags']}"
    )

  print("\n=== Final Structured JSON Output ===")
  print(json.dumps(all_extractions, indent=2))