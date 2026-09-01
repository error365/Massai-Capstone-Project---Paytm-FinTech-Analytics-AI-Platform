Paytm vertical: Money / Wealth advisory, plus a blockchain/crypto risk appendix.


Part A - Part A — Portfolio advisory agent (agentic think-act-observe pattern)

=== Advisory Agent Portfolio Recommendations ===
[INV01] Status: FINALIZED | Return: 9.20% | Volatility: 8.44%
 Narrative: For Conservative investor INV01, we recommend an allocation across ['PAYBOND', 'PAYGOLD', 'PAYRETAIL'] with an expected portfolio return of 9.2% and volatility of 8.4%.

[INV02] Status: FINALIZED | Return: 11.30% | Volatility: 12.57%
 Narrative: For Moderate investor INV02, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.3% and volatility of 12.6%.

[INV03] Status: ESCALATED_TO_HUMAN_ADVISOR | Return: 15.00% | Volatility: 20.58%
 Narrative: For Aggressive investor INV03, we recommend an allocation across ['PAYTECH', 'PAYFIN', 'PAYINFRA'] with an expected portfolio return of 15.0% and volatility of 20.6%.

[INV04] Status: FINALIZED | Return: 11.30% | Volatility: 12.57%
 Narrative: For Moderate investor INV04, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.3% and volatility of 12.6%.

[INV05] Status: ESCALATED_TO_HUMAN_ADVISOR | Return: 15.00% | Volatility: 20.58%
 Narrative: For Aggressive investor INV05, we recommend an allocation across ['PAYTECH', 'PAYFIN', 'PAYINFRA'] with an expected portfolio return of 15.0% and volatility of 20.6%.

 Part B - Structured disclosure extraction

 === Processing Corporate Disclosure Snippets ===
[doc_01] Sentiment: cautious | Hedging: True | Risks: []
[doc_02] Sentiment: neutral | Hedging: False | Risks: ['litigation']
[doc_03] Sentiment: neutral | Hedging: False | Risks: ['customer concentration']
[doc_04] Sentiment: cautious | Hedging: True | Risks: []
[doc_05] Sentiment: confident | Hedging: False | Risks: []
[doc_06] Sentiment: neutral | Hedging: False | Risks: ['regulatory']

=== Final Structured JSON Output ===
[
  {
    "doc_id": "doc_01",
    "risk_flags": [],
    "hedging_detected": true,
    "sentiment": "cautious"
  },
  {
    "doc_id": "doc_02",
    "risk_flags": [
      "litigation"
    ],
    "hedging_detected": false,
    "sentiment": "neutral"
  },
  {
    "doc_id": "doc_03",
    "risk_flags": [
      "customer concentration"
    ],
    "hedging_detected": false,
    "sentiment": "neutral"
  },
  {
    "doc_id": "doc_04",
    "risk_flags": [],
    "hedging_detected": true,
    "sentiment": "cautious"
  },
  {
    "doc_id": "doc_05",
    "risk_flags": [],
    "hedging_detected": false,
    "sentiment": "confident"
  },
  {
    "doc_id": "doc_06",
    "risk_flags": [
      "regulatory"
    ],
    "hedging_detected": false,
    "sentiment": "neutral"
  }
]

Part C — Multi-agent debate demo
=== Multi-Agent Investment Debate: PAYTECH ===
BULL AGENT:
With an analyst expected return of 19.0% against a beta of 1.55, PAYTECH offers attractive market-beating growth and systematic upside momentum.

BEAR AGENT:
However, with an annualized volatility (std dev) of 34.0% and a high beta of 1.55, PAYTECH carries significant downside risk and severe capital instability.

SYNTHESIZER:
While PAYTECH presents high potential upside with an expected return of 19.0%, its elevated volatility of 34.0% requires careful position sizing. Investors should balance its aggressive market sensitivity against their overall risk tolerance before committing capital.

Part D — DCF valuation calculator 

Base FCFF (Year 0): INR 350,000,000.00

--- DCF Sensitivity Matrix (Enterprise Value in INR Cr) ---
               Terminal g = 3.00%  Terminal g = 4.00%  Terminal g = 5.00%
WACC = 13.39%              539.90              581.62              633.28
WACC = 14.39%              489.95              523.16              563.44
WACC = 15.39%              448.15              475.04              507.11

Base DCF Enterprise Value: INR 523.16 Cr
EV/EBITDA (12.0x) Implied EV: INR 660.00 Cr

Part E — Blockchain/crypto risk-analysis appendix

* **Stablecoin Risk Management:** Demands surfacing clear structural distinctions between fiat-collateralized stablecoins (reserve opacity and custodian risks) and algorithmic stablecoins (death spiral vulnerabilities) to prevent retail investors from treating them as risk-free cash equivalents.


* **DeFi & DAO Governance Risks:** Warns against retail exposure to smart contract exploits, aggressive tokenomics dilution schedules, and governance hijacking by concentrated token whales.


* **Crypto Asset Allocation Recommendation:** Recommends a **0% baseline allocation** for Paytm Money retail portfolios based on CAPM/Modern Portfolio Theory principles, citing a lack of intrinsic cash flows/dividends, heavy-tailed crash risks, survivorship bias, high network friction, and tax drag (30% tax + 1% TDS).


* **Speculative Ceiling:** Advises capping any optional speculative crypto exposure at a strict maximum of **1% to 2% of net worth** strictly outside the core robo-advisory optimization engine.


* **Social Engineering Risk 1 (Authority Exploitation):** Highlights fake regulatory/law enforcement impersonation ("digital arrest") used to force urgent fund drawdowns. This is mitigated by bank-side real-time contextual velocity checks, active phone call detection, 30-minute cooling-off windows, and IVR voice verification.


* **Social Engineering Risk 2 (Greed & Temptation):** Highlights fake high-yield investment and cashback arbitrage scams targeting instant loan payouts. This is mitigated by closed-loop destination account restrictions on freshly disbursed loans and real-time receiving VPA fan-in graph modeling.

Portfolio Advisory Agent & Valuation System — README
1. Execution Mode Configuration (MOCK_LLM)
The system supports two execution modes controlled by the MOCK_LLM environment variable.

Default Graded Baseline (MOCK_LLM=1)
Mode: Fully deterministic mock mode.

Behavior: All components (advisory_agent.py, extract_disclosure.py, debate.py) execute using local rule engines, pre-configured formulas, and regex/keyword patterns. No external LLM API calls are made, requiring zero API keys and zero cost.

Run Transcripts Record: All output logs, structured JSON outputs, and portfolio recommendations recorded in the codebase transcripts were generated under MOCK_LLM=1.

# Run in default mock mode
export MOCK_LLM=1
python advisory_agent.py
python extract_disclosure.py
python dcf_calculator.py
python debate.py

