import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics import calinski_harabasz_score
from sklearn.preprocessing import StandardScaler

# --- 1. Isolation Forest Anomaly Detection ---
txn_df = pd.read_csv("txn_behaviour.csv")

# Extract and scale features
features = ["txn_hour", "is_new_device", "txn_amount_inr"]
X_txn_scaled = StandardScaler().fit_transform(txn_df[features])

# Contamination rate = 15 / 265
contamination_rate = 15.0 / len(txn_df)
iso_forest = IsolationForest(
    random_state=42, contamination=contamination_rate
)
txn_df["pred_anomaly"] = iso_forest.fit_predict(X_txn_scaled)

# Evaluate Recall
txn_df["is_flagged"] = (txn_df["pred_anomaly"] == -1).astype(int)
txn_df["is_ground_truth"] = txn_df["txn_id"].str.startswith("BTXNA").astype(int)

detected_count = len(
    txn_df[(txn_df["is_ground_truth"] == 1) & (txn_df["is_flagged"] == 1)]
)
print(f"Seeded Anomalies Total: 15")
print(f"Correctly Flagged Seeded Anomalies: {detected_count}")
print(f"Isolation Forest Recall: {(detected_count / 15.0) * 100:.2f}%")

# --- 2. Optional Stretch: K-Means Applicant Segmentation ---
applicants_df = pd.read_csv("credit_applicants.csv")
applicants_df["is_thin_file"] = applicants_df["credit_bureau_score"].isna().astype(
    int
)
applicants_df["credit_bureau_score"] = applicants_df[
    "credit_bureau_score"
].fillna(applicants_df["credit_bureau_score"].median())

X_app = pd.get_dummies(
    applicants_df.drop(columns=["applicant_id", "default"]),
    columns=["employment_type"],
    drop_first=True,
)
X_app_scaled = StandardScaler().fit_transform(X_app)

# Run K-Means with k=5 to observe over-indexing
km = KMeans(n_clusters=5, random_state=42, n_init=10)
applicants_df["cluster"] = km.fit_predict(X_app_scaled)

cluster_profile = (
    applicants_df.groupby("cluster")
    .agg(
        applicant_count=("applicant_id", "count"),
        defaults_count=("default", "sum"),
        default_rate_pct=("default", lambda x: round(x.mean() * 100, 2)),
    )
    .reset_index()
)

print("\nK-Means Applicant Clusters (k=5):")
print(cluster_profile)