import pandas as pd

# Load CSV files
merchants_df = pd.read_csv("merchants.csv")
users_df = pd.read_csv("users.csv")
ledger_df = pd.read_csv("ledger.csv")


def generate_insert_sql(df, table_name):
    columns = ", ".join(df.columns)
    rows = []
    for _, row in df.iterrows():
        vals = []
        for v in row:
            if pd.isna(v):
                vals.append("NULL")
            elif isinstance(v, (int, float)):
                vals.append(str(v))
            else:
                vals.append(f"'{str(v).replace('\'', '\'\'')}'")
        rows.append(f"({', '.join(vals)})")
    return (
        f"INSERT INTO {table_name} ({columns}) VALUES\n"
        + ",\n".join(rows)
        + ";\n"
    )


# Write to paytm_payments.sql
with open("paytm_payments.sql", "w") as f:
    f.write(generate_insert_sql(merchants_df, "merchants"))
    f.write(generate_insert_sql(users_df, "users"))
    f.write(generate_insert_sql(ledger_df, "transactions"))

print("SQL insert statements exported to paytm_payments.sql!")