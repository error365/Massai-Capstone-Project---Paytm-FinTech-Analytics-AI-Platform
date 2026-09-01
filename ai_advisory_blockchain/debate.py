import os
from typing import Dict

# Import stock universe parameters from project root
from stock_universe import STOCK_UNIVERSE  #[cite: 1]


def run_debate(ticker: str = "PAYTECH") -> Dict[str, str]:
  """Executes a 3-agent debate (Bull, Bear, Synthesizer) for a target stock ticker.

  Gated by MOCK_LLM environment variable (default: 1 for template-driven mock
  mode).
  """
  if ticker not in STOCK_UNIVERSE:
    raise ValueError(f"Ticker {ticker} not found in STOCK_UNIVERSE.")

  stock = STOCK_UNIVERSE[ticker]  #[cite: 1]
  beta = stock["beta"]  #[cite: 1]
  expected_return = stock["analyst_expected_return"]  #[cite: 1]
  std_dev = stock["std_dev"]  #[cite: 1]

  mock_mode = os.getenv("MOCK_LLM", "1") == "1"

  if mock_mode:
    # 1. Bull Agent Argument Formulation
    bull_arg = (
        f"With an analyst expected return of {expected_return:.1%} against a"
        f" beta of {beta:.2f}, {ticker} offers attractive market-beating"
        " growth and systematic upside momentum."
    )

    # 2. Bear Agent Argument Formulation
    bear_arg = (
        f"However, with an annualized volatility (std dev) of {std_dev:.1%}"
        f" and a high beta of {beta:.2f}, {ticker} carries significant downside"
        " risk and severe capital instability."
    )

    # 3. Synthesizer Agent Output (2-3 Sentence Balanced Summary)
    synthesizer_summary = (
        f"While {ticker} presents high potential upside with an expected return"
        f" of {expected_return:.1%}, its elevated volatility of {std_dev:.1%}"
        " requires careful position sizing. Investors should balance its"
        " aggressive market sensitivity against their overall risk tolerance"
        " before committing capital."
    )

    return {
        "ticker": ticker,
        "bull_agent": bull_arg,
        "bear_agent": bear_arg,
        "synthesizer": synthesizer_summary,
    }

  else:
    # Optional Live LLM API Call Path for Dynamic Debates
    pass


if __name__ == "__main__":
  target_ticker = "PAYTECH"
  debate_results = run_debate(target_ticker)

  print(f"=== Multi-Agent Investment Debate: {debate_results['ticker']} ===")
  print(f"🐂 BULL AGENT:\n{debate_results['bull_agent']}\n")
  print(f"🐻 BEAR AGENT:\n{debate_results['bear_agent']}\n")
  print(f"⚖️ SYNTHESIZER:\n{debate_results['synthesizer']}\n")