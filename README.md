Part 1 — Payments & Fraud Analytics (/payments_fraud_analytics)

Part A — Excel/Sheets merchant workbook

Open ledger.csv and merchants.csv in Excel/Google Sheets. Build a workbook merchant_workbook.xlsx with:
<span style="color: green;">
- Created merchant_workbook.xlsx and created below sheets inside this file
- Created transactions sheet and copied ledger.csv content here
- Created merchants sheet and copied merchants.csv content here
</span>

I. A VLOOKUP (fixed range with $ absolute references) that pulls each transaction's merchant_name, category, and region from the merchants sheet into a transactions-view sheet, using IFERROR/IFNA to show "Merchant not found" for any unmatched merchant_id.

<span style="color: green;">
Step 1 - Create three column in transactions sheet - merchant_name, category, region
Step 2 - Write the VLOOKUP Formulas as below for all three
1. =IFERROR(VLOOKUP(C2, merchants!$A$2:$D$41, 2, FALSE), "Merchant not found") - Merchant name column
2. =IFERROR(VLOOKUP(C2, merchants!$A$2:$D$41, 3, FALSE), "Merchant not found") - Category
3. =IFERROR(VLOOKUP(C2, merchants!$A$2:$D$41, 4, FALSE), "Merchant not found") - Region
</span>

II. An HLOOKUP demonstration on a small horizontally-laid-out reference table you add (e.g., a one-row-per-payment-method fee-tier lookup: UPI/Wallet/Card/Netbanking with their MDR-style fee percentages of your choosing, stated in the workbook).

<span style="color: green;">
 Step 1: Build the Horizontal Fee Table - created sheet name fee_structure
 Step 2 created Table headers as UPI, Wallet, Card and Netbanking 
 Step 3 Defined MDR rates for respective payment methods as 0 %, 1.5%, 2%, 1.85.
 Step 4 Created two new column in transactions sheet - mdr_fee_pct and fee_amount_inr
 Step 5 Write the HLOOKUP formula as 
 for mdr+fee_pct as =IFERROR(HLOOKUP(F2, fee_structure!$A$1:$D$2, 2, FALSE), 0) and 
 for fee_amount_inr as =E2 * L2
 </span>


III. A nested IF/AND classification column labeling each transaction "High-Value Merchant Day" when a merchant's daily transaction total (via a pivot table) exceeds INR 5,000 and its region is not "East", using distinct, documented cutoffs if you choose a different rule — state your exact rule in the workbook.

<span style="color: green;">
Step 1 - In transaction sheet added one more column name - txn_date, added the formula to convert transaction time to a date =INT(D2) 
Step 2 - format the Date (YYYY-MM-DD).
Step 3 - Created the daily_merchant_totals Pivot Table
Step 4 - Addd merchant_id and then txn_date as rows and amount_inr as value 
Step 5 - added new column merchant_daily_total and added =SUMIFS(E:E, C:C, C2, N:N, N2) formula to pull each transaction's corresponding daily total for that merchant
Step 6 - Wrote the Nested IF/AND Classification Formula - Rule Statement:

    Rule: Label a transaction as "High-Value Merchant Day" if merchant_daily_total > 5000 AND region <> "East". Otherwise, label it "Standard".

Step 7 - Added new column in transaction sheet as day_classification
Step 8 - Use below formula to find Wheter the transaction is standard or High value merchant day
=IF(AND(O2>5000, K2<>"East"), "High-Value Merchant Day", "Standard")
</span>


IV. A pivot table summarizing total amount_inr and count of transactions by merchant_id and status, plus a count-vs-count-unique comparison (unique days transacted vs. total transaction count) for at least 5 merchants.

<span style="color: green;">
Step 1 - Select the transaction table and insert a new Pivot table and create a new sheet named merchant_pivot_summary
Step 2 - add row as merchant_id
Step 3 - add column as status
Step 4 - add values as amount_inr, transaction_id
Step 5 - created three column in this sheet as merchant_id, total_txn_count and unique_days_transacted 
Step 5 - total_txn_count formula as =COUNTIF(transactions!$C:$C, K4) and unique days transacted as =COUNT(UNIQUE(FILTER(transactions!$N:$N, transactions!$C:$C=k4)))

    you will observe that for active merchants, total_txn_count is greater than unique_days_transacted, indicating multiple transactions occurred on single calendar days
</span>
