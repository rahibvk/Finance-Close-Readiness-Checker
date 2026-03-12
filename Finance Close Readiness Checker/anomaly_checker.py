import pandas as pd
import os

# -----------------------------
# 1. Load dataset
# -----------------------------
file_path = "finance_data.csv"   # change path if needed
df = pd.read_csv(file_path)

# -----------------------------
# 2. Clean column names
# -----------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# -----------------------------
# 3. Remove fully blank rows
# -----------------------------
df = df.dropna(how="all")

# -----------------------------
# 4. Convert numeric columns
# -----------------------------
numeric_cols = [
    "units_sold",
    "manufacturing_price",
    "sale_price",
    "gross_sales",
    "discounts",
    "sales",
    "cogs",
    "profit"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# 5. Convert date column
# -----------------------------
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -----------------------------
# 6. Create profit margin
# -----------------------------
df["profit_margin"] = df["profit"] / df["sales"]

# -----------------------------
# 7. Create anomaly flags
# -----------------------------
df["flag_missing_sales"] = df["sales"].isna()
df["flag_negative_profit"] = df["profit"] < 0
df["flag_profit_margin_anomaly"] = (df["profit_margin"] < 0) | (df["profit_margin"] > 0.6)

# Any flagged row
df["is_flagged"] = (
    df["flag_missing_sales"] |
    df["flag_negative_profit"] |
    df["flag_profit_margin_anomaly"]
)

# -----------------------------
# 8. Summary metrics
# -----------------------------
total_revenue = df["sales"].sum()
missing_sales_count = df["flag_missing_sales"].sum()
negative_profit_count = df["flag_negative_profit"].sum()
profit_margin_anomalies = df["flag_profit_margin_anomaly"].sum()
flagged_records_count = df["is_flagged"].sum()

# -----------------------------
# 9. Export flagged records
# -----------------------------
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

flagged_records = df[df["is_flagged"]].copy()
flagged_file = os.path.join(output_folder, "flagged_records.csv")
flagged_records.to_csv(flagged_file, index=False)

# -----------------------------
# 10. Generate clean report text
# -----------------------------
status = "Review Required" if flagged_records_count > 0 else "Ready for Close"

report_text = f"""Finance Close Summary
---------------------
Total Revenue: ${total_revenue:,.2f}

Data Quality Checks:
Missing Sales Records: {missing_sales_count}
Negative Profit Records: {negative_profit_count}
Profit Margin Anomalies: {profit_margin_anomalies}

Total Records Flagged for Review: {flagged_records_count}

Close Readiness Status: {status}
"""

report_file = os.path.join(output_folder, "finance_close_summary.txt")
with open(report_file, "w", encoding="utf-8") as f:
    f.write(report_text)

# -----------------------------
# 11. Print final output
# -----------------------------
print(report_text)
print(f"Flagged records exported to: {flagged_file}")
print(f"Summary report saved to: {report_file}")