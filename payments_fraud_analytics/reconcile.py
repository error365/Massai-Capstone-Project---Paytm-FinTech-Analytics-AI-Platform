import pandas as pd


def reconcile_payments(ledger_df, gateway_df):
    """Reconciles internal payment ledger against payment gateway exports.

    Returns:
        tuple: (missing_in_gateway, missing_in_ledger, amount_mismatches,
        status_mismatches)
    """
    # 1. Set operations for primary key ID matching
    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])

    # IDs present in ledger but missing in gateway export
    missing_gw_ids = ledger_ids - gateway_ids
    missing_in_gateway = ledger_df[
        ledger_df["transaction_id"].isin(missing_gw_ids)
    ].copy()

    # IDs present in gateway export but missing in ledger
    missing_led_ids = gateway_ids - ledger_ids
    missing_in_ledger = gateway_df[
        gateway_df["transaction_id"].isin(missing_led_ids)
    ].copy()

    # 2. Pairwise comparison using pd.merge on common IDs
    common_ids = ledger_ids & gateway_ids

    common_ledger = ledger_df[ledger_df["transaction_id"].isin(common_ids)]
    common_gateway = gateway_df[gateway_df["transaction_id"].isin(common_ids)]

    merged = pd.merge(
        common_ledger,
        common_gateway,
        on="transaction_id",
        suffixes=("_ledger", "_gateway"),
    )

    # 3. Calculate Amount Mismatches (with computed difference)
    merged["amount_diff"] = (
        merged["amount_inr_ledger"] - merged["amount_inr_gateway"]
    )
    amount_mismatches = merged[merged["amount_diff"] != 0].copy()

    # 4. Calculate Status Mismatches
    status_mismatches = merged[
        merged["status_ledger"] != merged["status_gateway"]
    ].copy()

    return (
        missing_in_gateway,
        missing_in_ledger,
        amount_mismatches,
        status_mismatches,
    )

# Load CSV datasets
ledger_df = pd.read_csv("ledger.csv")
gateway_df = pd.read_csv("gateway_export.csv")

# Run reconciliation
missing_gw, missing_led, amt_mismatch, status_mismatch = reconcile_payments(
    ledger_df, gateway_df
)

# Print execution summary
print("=" * 55)
print("PAYMENT RECONCILIATION DISCREPANCY REPORT")
print("=" * 55)
print(f"Total Transactions in Ledger:  {len(ledger_df)}")
print(f"Total Transactions in Gateway: {len(gateway_df)}\n")

print(
    f"1. Missing in Gateway: {len(missing_gw):3d} rows ({len(missing_gw)/len(ledger_df):.2%})"
)
print(
    f"2. Missing in Ledger:  {len(missing_led):3d} rows ({len(missing_led)/len(ledger_df):.2%})"
)
print(
    f"3. Amount Mismatches:  {len(amt_mismatch):3d} rows ({len(amt_mismatch)/len(ledger_df):.2%})"
)
print(
    f"4. Status Mismatches:  {len(status_mismatch):3d} rows ({len(status_mismatch)/len(ledger_df):.2%})"
)
print("=" * 55)