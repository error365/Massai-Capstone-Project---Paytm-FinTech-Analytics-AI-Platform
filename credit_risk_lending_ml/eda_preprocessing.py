import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.tree import DecisionTreeClassifier

# 1. Load Data & Compute EDA Metrics
df = pd.read_csv("credit_applicants.csv")
print(f"Measured Default Rate: {df['default'].mean() * 100:.2f}%")
print(
    "Missing Bureau Scores:"
    f" {df['credit_bureau_score'].isna().mean() * 100:.2f}%"
)

# Create thin file flag
df["is_thin_file"] = df["credit_bureau_score"].isna().astype(int)

# 2. Train/Test Split
X = df.drop(columns=["applicant_id", "default"])
y = df["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Median Imputation (Train only)
bureau_median = X_train["credit_bureau_score"].median()  # Evaluates to 612.0
X_train["credit_bureau_score"] = X_train["credit_bureau_score"].fillna(
    bureau_median
)
X_test["credit_bureau_score"] = X_test["credit_bureau_score"].fillna(
    bureau_median
)

# 4. One-Hot Encoding
X_train = pd.get_dummies(X_train, columns=["employment_type"], drop_first=True)
X_test = pd.get_dummies(X_test, columns=["employment_type"], drop_first=True)
X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

# 5. Scaling
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
)
X_test_scaled = pd.DataFrame(
    scaler.transform(X_test), columns=X_test.columns, index=X_test.index
)

#Part 2 - classification model

# 1. Fit Models
log_reg = LogisticRegression(random_state=42).fit(X_train_scaled, y_train)
dt_clf = DecisionTreeClassifier(random_state=42).fit(X_train_scaled, y_train)

# 2. Get Test Predictions & Probabilities
y_pred_lr = log_reg.predict(X_test_scaled)
y_prob_lr = log_reg.predict_proba(X_test_scaled)[:, 1]

y_pred_dt = dt_clf.predict(X_test_scaled)
y_prob_dt = dt_clf.predict_proba(X_test_scaled)[:, 1]

# 3. Build Risk-Based Pricing Table on Test Set
test_df = pd.DataFrame(
    {"actual_default": y_test, "pred_default_prob": y_prob_lr}
)

test_df["risk_tier"] = pd.qcut(
    test_df["pred_default_prob"],
    q=4,
    labels=[
        "Tier 1 (Low Risk)",
        "Tier 2 (Medium Risk)",
        "Tier 3 (High Risk)",
        "Tier 4 (Very High Risk)",
    ],
)

pricing_table = (
    test_df.groupby("risk_tier", observed=False)
    .agg(
        applicant_count=("pred_default_prob", "count"),
        min_prob=("pred_default_prob", "min"),
        max_prob=("pred_default_prob", "max"),
        actual_defaults=("actual_default", "sum"),
        actual_default_rate=("actual_default", "mean"),
    )
    .reset_index()
)

pricing_table["actual_default_rate_pct"] = (
    pricing_table["actual_default_rate"] * 100
).round(2)
pricing_table["suggested_interest_rate"] = [
    "12.0% - 14.0%",
    "15.0% - 18.0%",
    "19.0% - 24.0%",
    "25.0% - 30.0%",
]

print(
    pricing_table[
        [
            "risk_tier",
            "applicant_count",
            "min_prob",
            "max_prob",
            "actual_default_rate_pct",
            "suggested_interest_rate",
        ]
    ]
)