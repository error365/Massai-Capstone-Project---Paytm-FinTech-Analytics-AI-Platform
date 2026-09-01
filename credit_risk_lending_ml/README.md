Part 2 — Credit Risk & Lending ML
==================================
Task 1: Exploratory Data Analysis (EDA) & is_thin_file Flag

Load Data: Read credit_applicants.csv into a Pandas DataFrame.Report Summary Metrics:Measured Default Rate: 20.25% (81 defaults out of 400 applicants), falling within the target 15–25% range.Missing Bureau Scores: 20.00% (80 out of 400 applicants) representing new-to-credit thin-file applicants.Engineer Flag: Create a binary flag column is_thin_file:$$\text{is\_thin\_file} = \begin{cases} 1 & \text{if } \text{credit\_bureau\_score} \text{ is missing} \\ 0 & \text{otherwise} \end{cases}$$Note: This flag relies purely on raw missingness status and is safe to construct prior to train/test splitting without risk of data leakage.

Task 2: Stratified Train/Test Split & Preprocessing Pipeline

Step 2.1 — Stratified Split & Justification  Split the dataset into 75% training ($N=300$) and 25% testing ($N=100$) using random_state=42 and stratify=y.  Stratification Justification: Because default events are imbalanced (20.25% defaults vs. 79.75% non-defaults), random splitting could cause class imbalance skew between train and test sets. Stratification guarantees both train and test splits retain the exact 20.25% target default ratio.  

Step 2.2 — Train-Only Median Imputation & JustificationCompute the median credit_bureau_score strictly on the training set: 612.00.Impute missing values in both X_train and X_test using 612.00.Alternate-Data Imputation Justification: Computing the median strictly from X_train prevents test-set target leakage. Combining this imputed median with is_thin_file = 1 allows alternate Paytm data signals (e.g., UPI inflow, transaction history) to drive risk evaluation for thin-file applicants while maintaining a baseline bureau score.

Step 2.3 — Categorical EncodingApply One-Hot Encoding (pd.get_dummies) to employment_type with drop_first=True to avoid multicollinearity.Align train and test column structures to maintain feature parity across both sets.Step 

2.4 — StandardScaler FittingInitialize StandardScaler() and fit strictly on X_train.Transform both X_train and X_test using the training-fitted mean and variance parameters ($\mu_{train}, \sigma_{train}$).

Measured Default Rate: 20.25%
Missing Bureau Scores: 20.00%

Task 2 - Classification models
Risk Tier,Probability Range (p^​),Applicant Count,Actual Defaults,Actual Default Rate (%),Illustrative Interest Rate
Tier 1 (Low Risk),0.0049≤p^​≤0.0358,25,2,8.00%,12.0% – 14.0%
Tier 2 (Medium Risk),0.0363≤p^​≤0.1461,25,3,12.00%,15.0% – 18.0%
Tier 3 (High Risk),0.1506≤p^​≤0.3377,25,5,20.00%,19.0% – 24.0%
Tier 4 (Very High Risk),0.3516≤p^​≤0.9469,25,10,40.00%,25.0% – 30.0%

Task 3 - Anomaly detection and optional segmentation
Seeded Anomalies Total: 15
Correctly Flagged Seeded Anomalies: 11
Isolation Forest Recall: 73.33%

K-Means Applicant Clusters (k=5):
   cluster  applicant_count  defaults_count  default_rate_pct
0        0               64               6              9.38
1        1               73              24             32.88
2        2              114              26             22.81
3        3               86              10             11.63
4        4               63              15             23.81

Task 4 - Bias-Awareness Note & Governance Recommendation
Even without explicit demographic fields like gender, age, or location in the dataset, features like employment_type, monthly_income_inr, and credit_bureau_score can act as indirect proxy variables for protected attributes in real-world deployments. Structural economic disparities mean self-employed, gig-economy, or informal workers—who are disproportionately women, youth, or rural residents—often show lower formal incomes and non-existent bureau records due to historical financial exclusion rather than poor creditworthiness. Heavy reliance on traditional bureau scores inherently penalizes "thin-file" applicants, perpetuating systemic barriers to credit access.

To mitigate proxy discrimination and algorithmic bias before going live, Paytm Postpaid should implement two key governance steps:

Disparate Impact Audits: Conduct regular demographic parity and equal opportunity audits across income and employment strata to ensure approval ratios do not systematically disadvantage vulnerable groups.

Maker-Checker Human-in-the-Loop Review: Establish a human-in-the-loop review policy specifically for declined thin-file (is_thin_file = 1) applicants. Instead of automated rejections, flag border-case thin-file applicants for manual underwriter review. Underwriters can evaluate alternative data signals—such as Paytm UPI transaction regularity and wallet inflows—to grant fair access while maintaining sound risk management.

2. Final Model-Comparison Table & Deployment Recommendation
Overall System Metric Summary

Model / Sub-Task,Model Type,Accuracy,Precision,Recall,F1-Score,ROC-AUC / Recall
Credit Default Model 1,Logistic Regression,83.00%,63.64%,35.00%,45.16%,0.719 (AUC)
Credit Default Model 2,Decision Tree Classifier,70.00%,28.57%,30.00%,29.27%,0.519 (AUC)
Fraud Anomaly Detection,Isolation Forest,—,—,73.33%,—,73.33% (Recall)

Deployment Recommendation
I recommend deploying Logistic Regression for Paytm Postpaid's primary default prediction pipeline over the Decision Tree Classifier. Logistic Regression demonstrates superior overall performance with higher Accuracy (83.00% vs. 70.00%), Precision (63.64% vs. 28.57%), F1-Score (45.16% vs. 29.27%), and ROC-AUC (0.719 vs. 0.519). Crucially, Logistic Regression outputs smooth, well-calibrated class probabilities that enable monotonic risk-based interest rate pricing tiers, whereas the unpruned Decision Tree overfits the training data and achieves near-random discrimination on test data. Coupled with the Isolation Forest model (which successfully catches 73.33% of behavioral fraud anomalies), this architecture provides a balanced, interpretable, and effective risk management system.