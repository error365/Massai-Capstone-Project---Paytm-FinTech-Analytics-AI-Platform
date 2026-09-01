import math
import os

# 1. Direct Imports from Separate Project Files
from disclosure_snippets import DISCLOSURE_SNIPPETS  #[cite: 1]
from investor_profiles import INVESTOR_PROFILES  #[cite: 2]
from stock_universe import (  #[cite: 3]
    MARKET_RETURN,
    RISK_FREE_RATE,
    STOCK_UNIVERSE,
)

# 2. Portfolio Allocation Mapping
ALLOCATION_MAP = {
    "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],  #[cite: 2, 3]
    "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],  #[cite: 2, 3]
    "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],  #[cite: 2, 3]
}
RHO = 0.3  # Pairwise correlation


# Tool Call Function accessing imported STOCK_UNIVERSE
def get_stock_data(ticker: str) -> dict:
  return STOCK_UNIVERSE[ticker]  #[cite: 3]


class AdvisoryAgent:

  def run(self, profile: dict) -> dict:
    investor_id = profile["investor_id"]  #[cite: 2]
    risk = profile["risk_tolerance"]  #[cite: 2]

    # Think: Allocation selection
    tickers = ALLOCATION_MAP[risk]

    # Act: Retrieve tool data using imported STOCK_UNIVERSE
    stock_data = {t: get_stock_data(t) for t in tickers}

    # Observe: Calculate CAPM & Variance
    w = 1.0 / 3.0
    capm_returns = [
        RISK_FREE_RATE
        + stock_data[t]["beta"] * (MARKET_RETURN - RISK_FREE_RATE)
        for t in tickers
    ]  #[cite: 3]
    std_devs = [stock_data[t]["std_dev"] for t in tickers]  #[cite: 3]

    port_er = sum(w * r for r in capm_returns)

    var_sum = sum((w**2) * (sd**2) for sd in std_devs)
    cov_sum = 0.0
    for i in range(len(tickers)):
      for j in range(i + 1, len(tickers)):
        cov_sum += 2 * w * w * (RHO * std_devs[i] * std_devs[j])

    port_vol = math.sqrt(var_sum + cov_sum)
    is_escalated = port_vol > 0.20

    # Narrative generation
    narrative = (
        f"For {risk} investor {investor_id}, we recommend an allocation"
        f" across {tickers} with an expected portfolio return of"
        f" {port_er:.1%} and volatility of {port_vol:.1%}."
    )

    return {
        "investor_id": investor_id,
        "risk_tolerance": risk,
        "tickers": tickers,
        "expected_return": round(port_er, 4),
        "volatility": round(port_vol, 4),
        "status": "ESCALATED_TO_HUMAN_ADVISOR" if is_escalated else "FINALIZED",
        "narrative": narrative,
    }


# Execute using imported INVESTOR_PROFILES list
if __name__ == "__main__":
  agent = AdvisoryAgent()

  print("=== Advisory Agent Portfolio Recommendations ===")
  for profile in INVESTOR_PROFILES:  #[cite: 2]
    result = agent.run(profile)
    print(
        f"[{result['investor_id']}] Status: {result['status']} | Return:"
        f" {result['expected_return']:.2%} | Volatility:"
        f" {result['volatility']:.2%}"
    )
    print(f" Narrative: {result['narrative']}\n")