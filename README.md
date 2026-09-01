# Paytm FinTech Analytics & AI Platform — Capstone Project

This repository contains the end-to-end implementation for the **Paytm FinTech Analytics & AI Platform Capstone Project**, covering payment fraud analytics, credit risk machine learning, and AI-assisted wealth advisory with blockchain risk governance.

---

## 🛠️ Repository Structure & Setup

Project dependencies can be installed using either directory-specific `requirements.txt` files or a single consolidated root `requirements.txt`.

### Requirements File Structure
* **Consolidated Root Requirements (`/requirements.txt`):** Recommended for single-environment execution covering all parts.
* **Modular Requirements (Per Part):**
  * `payments_fraud_analytics/requirements.txt`
  * `credit_risk_lending_ml/requirements.txt`
  * `wealth_advisory_crypto/requirements.txt`

### Installation
```bash
# Clone the repository
git clone [https://github.com/error365/Massai-Capstone-Project---Paytm-FinTech-Analytics-AI-Platform.git](https://github.com/error365/Massai-Capstone-Project---Paytm-FinTech-Analytics-AI-Platform.git)
cd Massai-Capstone-Project---Paytm-FinTech-Analytics-AI-Platform


# Install dependencies via consolidated requirements file
pip install -r requirements.txt




====================================================================

How to Run End-to-End

Part 1: Payment Fraud Analytics & Anomaly Detection

terminal
cd payments_fraud_analytics
py anomaly_detection.py

Outputs: Evaluates Isolation Forest against seeded ground-truth anomalies (BTXNA), outputs recall metrics, and prints candidate default clusters via K-Means.

Part 2: Credit Risk Lending ML Pipeline

terminal
cd credit_risk_lending_ml
py credit_risk_pipeline.py

Outputs: Fits Logistic Regression and Decision Tree models on credit applicant data, prints Accuracy, Precision, Recall, F1-Score, and ROC-AUC metrics, and outputs the baseline evaluation tables.

Part 3: Paytm Money Wealth Advisory & DCF Valuation

terminal
cd wealth_advisory_crypto

#Default Graded Offline Baseline (Mock Mode)
export MOCK_LLM=1
py advisory_agent.py
py extract_disclosure.py
py dcf_calculator.py
py debate.py

# Design Decisions & Interpretations

# Part A: Payment Fraud & Behavioral Anomaly Detection

# Isolation Forest Scaling: Standardized numeric behavioral features (txn_hour, is_new_device, txn_amount_inr) and matched the model contamination parameter exactly to the ground-truth anomaly ratio ($15 / 265 \approx 5.66\\%$).

# Recall Performance: Achieved 73.33% recall ($11/15$) against seeded ground-truth anomalies (BTXNA prefix).

# K-Means Segmentation: Identified optimal $k=2$ and $k=5$ cluster distributions via the Calinski-Harabasz index. Granular clustering ($k=5$) revealed an over-indexing default segment (32.88% default rate, $1.62\times$ baseline).

# Part B: Credit Risk & Lending ML ModelingModel 

# Selection: Logistic Regression significantly outperforms Decision Trees across all primary metrics:Accuracy: 83.00% vs 70.00%Precision: 63.64% vs 28.57%F1-Score: 45.16% vs 29.27%ROC-AUC: 0.719 vs 0.519

# Governance & Proxy Bias: Addressed how employment_type, monthly_income_inr, and credit_bureau_score act as proxy variables for protected attributes (gender, age, location). Recommended Disparate Impact Audits and a Human-in-the-Loop (Maker-Checker) policy for declined thin-file applicants (is_thin_file=1).

# Part C: Wealth Advisory, DCF Valuation & Crypto RiskPortfolio Advisory Agent: Built around the Think-Act-Observe pattern. Automatically flags and escalates high-risk portfolios ($\sigma_p > 20\\%$) to human advisors (triggered for Aggressive profiles: INV03, INV05 at 20.58% volatility).

# DCF Valuation & Sensitivity: Evaluated FCFF (Base: ₹35.0 Cr) with a calculated WACC of 14.39% ($\beta = 1.55$). Verified the self-check constraint ($\text{WACC} - g \ge 1.0\\%$ spread in all 9 grid cells) with a worst-case spread of 8.39%. Calculated intrinsic EV at ₹523.16 Cr vs. ₹660.00 Cr under EV/EBITDA multiple ($12.0\times$).

# Crypto Risk Appendix: Recommended 0% baseline allocation for retail Paytm Money portfolios due to zero intrinsic cash flow, fat-tail downside risks, and high tax drag (30% tax + 1% TDS). Addressed T.A.N.G. fraud vectors with bank-side real-time defenses.⚙️ Execution Mode & API Usage (MOCK_LLM)Default Mode (MOCK_LLM=1): Completely deterministic and offline. Uses rule engines and template generators for grading. No network calls or API keys required.

