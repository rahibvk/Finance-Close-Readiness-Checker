# Finance Close Readiness Checker

## Project Overview

This project simulates a **month-end financial data validation process** used by finance teams before closing the books. The system checks financial transaction data for data quality issues and anomalies before reporting.

The workflow combines **PostgreSQL (SQL)** for rule-based data validation and **Python (Pandas)** for anomaly detection and summary generation.

The project identifies missing values, negative profit transactions, duplicate records, and abnormal profit margins, then produces a **Finance Close Summary Report**.

---

## Tech Stack

- **PostgreSQL** – Data storage  
- **SQL** – Data validation checks  
- **Python (Pandas)** – Data analysis and anomaly detection  
- **Excel / CSV** – Raw financial dataset  

---

## Dataset

The project uses a financial sample dataset with the following columns:

- Segment  
- Country  
- Product  
- Discount Band  
- Units Sold  
- Manufacturing Price  
- Sale Price  
- Gross Sales  
- Discounts  
- Sales  
- COGS  
- Profit  
- Date  
- Month Number  
- Month Name  
- Year  

These fields represent typical financial metrics used in revenue and profitability analysis.

---

## Project Workflow
Raw Finance Data (Excel / CSV)
↓
PostgreSQL Database
(SQL Data Validation)
↓
Python Analysis (Pandas)
(Anomaly Detection)
↓
Finance Close Summary Report
---

## SQL Data Validation

SQL is used to validate the dataset before performing analysis.

### Missing Sales Values

```sql
SELECT COUNT(*) AS missing_sales_count
FROM public.finance_data
WHERE sales IS NULL;
Negative Profit Records
SELECT COUNT(*) AS negative_profit_count
FROM public.finance_data
WHERE profit < 0;
Duplicate Transactions
SELECT
    date,
    country,
    product,
    sales,
    profit,
    COUNT(*) AS duplicate_count
FROM public.finance_data
GROUP BY date, country, product, sales, profit
HAVING COUNT(*) > 1;
Clean Data View

A cleaned dataset is created to remove fully blank rows before analysis.

CREATE OR REPLACE VIEW public.finance_data_clean AS
SELECT *
FROM public.finance_data
WHERE NOT (
    date IS NULL
    AND country IS NULL
    AND product IS NULL
    AND sales IS NULL
    AND profit IS NULL
);
Python Analysis

Python is used to detect anomalies and generate summary reports.

The Python script performs the following:

Loads the financial dataset

Cleans column names

Removes blank rows

Converts numeric columns

Converts the date column

Calculates profit margin

Flags suspicious records

Exports flagged transactions

Generates a summary report

Profit Margin Formula
profit_margin = profit / sales
Anomaly Rules

Records are flagged when:

Sales value is missing

Profit is negative

Profit margin < 0

Profit margin > 0.6

Output Files

The project automatically generates two output files.

Flagged Records
output/flagged_records.csv

Contains transactions flagged for review along with anomaly indicators.

Finance Close Summary
output/finance_close_summary.txt

Example output:

Finance Close Summary
---------------------
Total Revenue: $119,920,182.26

Data Quality Checks:
Missing Sales Records: 0
Negative Profit Records: 58
Profit Margin Anomalies: 159

Total Records Flagged for Review: 159

Close Readiness Status: Review Required


How to Run the Project
1. Import the dataset into PostgreSQL

Create a table named finance_data and import the cleaned CSV dataset.

2. Run SQL validation queries

Run the queries inside:

sql/validation_checks.sql
3. Run the Python script
python anomaly_checker.py
4. Review outputs

The script will generate:

output/flagged_records.csv
output/finance_close_summary.txt
Key Results
Metric	Result
Total Revenue	$119,920,182
Negative Profit Records	58
Profit Margin Anomalies	159
Records Flagged for Review	159

These results indicate several transactions require review before final financial reporting.

Business Value

This project demonstrates how data validation and anomaly detection can support finance teams by:

identifying data quality issues before reporting

highlighting unusual financial transactions

improving reporting accuracy

generating automated validation reports before month-end close

Author

Rahib
