# 💳 Payment Portal Reconciliation 

<div align="center">

# 🏦 Automated Payment Reconciliation System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-Transaction_Data-green?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Ubuntu_20.04+-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![FinTech](https://img.shields.io/badge/FinTech-Reconciliation-blue?style=for-the-badge)

### 🔄 Parse • Match • Reconcile • Report

</div>

---

# 📖 Overview

Financial systems often receive transaction data from multiple sources:

* 💳 Payment Portals
* 🏦 Banking Systems
* 🌐 Payment Gateways
* 📊 Settlement Platforms

Reconciling transactions manually is time-consuming and error-prone.

This lab demonstrates how to build an automated reconciliation system capable of:

✅ Parsing transaction records

✅ Normalizing data formats

✅ Detecting discrepancies

✅ Identifying missing transactions

✅ Generating audit-ready reports

---

# 🎯 Learning Objectives

By completing this lab, you will:

* 🔄 Automate transaction reconciliation
* 📄 Parse multiple CSV formats
* ⚖️ Match records across systems
* 🚨 Detect discrepancies automatically
* 📊 Generate reconciliation reports
* 🛡️ Handle financial data edge cases

---

# 📋 Prerequisites

| Requirement         | Description                    |
| ------------------- | ------------------------------ |
| 🐍 Python           | Functions, loops, dictionaries |
| 📄 CSV              | File handling basics           |
| 🖥 Linux            | Command-line operations        |
| 📊 Data Structures  | Lists, sets, dictionaries      |
| 🔍 Comparison Logic | Matching records               |

---

# 🏗️ System Architecture

```text
                ┌──────────────────┐
                │ Portal CSV Data  │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Transaction      │
                │ Parser           │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Reconciliation   │
                │ Engine           │
                └─────────┬────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   Exact Matches   Discrepancies   Missing Records
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                ┌──────────────────┐
                │ Report Generator │
                └──────────────────┘
```

---

# 🚀 Environment Setup

## Step 1: Start Lab Environment

Provision your Linux machine and connect via SSH.

---

## Step 2: Install Required Tools

```bash
sudo apt update

sudo apt install -y python3 python3-pip

pip3 install pandas tabulate
```

---

## Step 3: Create Project Directory

```bash
mkdir ~/payment-reconciliation

cd ~/payment-reconciliation
```

---

# 📂 Task 1: Parse Transaction Records

---

# 📝 Step 1: Create Sample Data

## Portal Transactions

```bash
cat > portal_transactions.csv << 'EOF'
transaction_id,date,amount,customer_id,status,payment_method
TXN001,2024-01-15,150.00,CUST101,completed,credit_card
TXN002,2024-01-15,75.50,CUST102,completed,paypal
TXN003,2024-01-16,200.00,CUST103,completed,debit_card
TXN004,2024-01-16,89.99,CUST104,completed,credit_card
TXN005,2024-01-17,125.00,CUST105,failed,paypal
TXN006,2024-01-17,300.00,CUST106,completed,credit_card
EOF
```

---

## Bank Transactions

```bash
cat > bank_transactions.csv << 'EOF'
reference,transaction_date,settled_amount,account_ref,payment_type
TXN001,2024-01-15,150.00,CUST101,CC
TXN002,2024-01-15,75.50,CUST102,PP
TXN003,2024-01-16,200.00,CUST103,DC
TXN004,2024-01-16,88.99,CUST104,CC
TXN006,2024-01-17,300.00,CUST106,CC
TXN007,2024-01-18,450.00,CUST107,CC
EOF
```

---

# 🏗️ Step 2: Create Transaction Parser

Create:

```bash
nano transaction_parser.py
```

---

## transaction_parser.py

```python
import pandas as pd

class TransactionParser:

    def __init__(self):
        self.portal_data = None
        self.bank_data = None

    def load_portal_transactions(self, filepath):

        df = pd.read_csv(filepath)

        df = df[df["status"] == "completed"]

        df = df.rename(columns={
            "transaction_id": "id",
            "date": "date",
            "amount": "amount",
            "customer_id": "customer"
        })

        df["amount"] = df["amount"].astype(float)

        return df[["id", "date", "amount", "customer"]]

    def load_bank_transactions(self, filepath):

        df = pd.read_csv(filepath)

        df = df.rename(columns={
            "reference": "id",
            "transaction_date": "date",
            "settled_amount": "amount",
            "account_ref": "customer"
        })

        df["amount"] = df["amount"].astype(float)

        return df[["id", "date", "amount", "customer"]]

    def get_transaction_summary(self, df):

        return {
            "count": len(df),
            "total_amount": df["amount"].sum(),
            "avg_amount": df["amount"].mean()
        }
```

---

# 📊 Task 2: Match Entries & Detect Discrepancies

---

# ⚙️ Step 1: Create Reconciliation Engine

Create:

```bash
nano reconciliation_engine.py
```

---

## reconciliation_engine.py

```python
import pandas as pd

class ReconciliationEngine:

    def __init__(self, portal_df, bank_df):

        self.portal_df = portal_df
        self.bank_df = bank_df

    def find_exact_matches(self):

        merged = pd.merge(
            self.portal_df,
            self.bank_df,
            on="id",
            suffixes=("_portal", "_bank")
        )

        matches = merged[
            abs(
                merged["amount_portal"] -
                merged["amount_bank"]
            ) < 0.01
        ]

        return matches.to_dict("records")

    def find_amount_discrepancies(self, tolerance=0.01):

        merged = pd.merge(
            self.portal_df,
            self.bank_df,
            on="id",
            suffixes=("_portal", "_bank")
        )

        discrepancies = merged[
            abs(
                merged["amount_portal"] -
                merged["amount_bank"]
            ) > tolerance
        ]

        return discrepancies.to_dict("records")

    def find_unmatched_transactions(self):

        portal_ids = set(
            self.portal_df["id"]
        )

        bank_ids = set(
            self.bank_df["id"]
        )

        portal_only = list(
            portal_ids - bank_ids
        )

        bank_only = list(
            bank_ids - portal_ids
        )

        return portal_only, bank_only

    def reconcile(self):

        matched = self.find_exact_matches()

        discrepancies = self.find_amount_discrepancies()

        portal_only, bank_only = \
            self.find_unmatched_transactions()

        return {

            "matched": matched,

            "discrepancies": discrepancies,

            "unmatched_portal": portal_only,

            "unmatched_bank": bank_only
        }
```

---

# 📑 Task 3: Generate Reconciliation Report

---

# 📝 Step 1: Create Report Generator

Create:

```bash
nano report_generator.py
```

---

## report_generator.py

```python
from tabulate import tabulate
from datetime import datetime

class ReportGenerator:

    def __init__(self, results):

        self.results = results

    def generate_summary_section(self):

        matched = len(
            self.results["matched"]
        )

        discrepancies = len(
            self.results["discrepancies"]
        )

        total = matched + discrepancies

        rate = (
            matched / total * 100
        ) if total else 0

        return f"""
=== SUMMARY ===

Matched: {matched}
Discrepancies: {discrepancies}

Reconciliation Rate:
{rate:.2f}%
"""

    def generate_discrepancy_table(self):

        rows = []

        for item in self.results["discrepancies"]:

            rows.append([
                item["id"],
                item["amount_portal"],
                item["amount_bank"],
                round(
                    item["amount_portal"] -
                    item["amount_bank"],
                    2
                )
            ])

        return tabulate(
            rows,
            headers=[
                "ID",
                "Portal",
                "Bank",
                "Difference"
            ],
            tablefmt="grid"
        )

    def generate_unmatched_section(self):

        return f"""

=== PORTAL ONLY ===
{self.results['unmatched_portal']}

=== BANK ONLY ===
{self.results['unmatched_bank']}
"""

    def save_report(self, filename):

        report = f"""
PAYMENT RECONCILIATION REPORT
Generated:
{datetime.now()}

{self.generate_summary_section()}

{self.generate_discrepancy_table()}

{self.generate_unmatched_section()}
"""

        with open(filename, "w") as f:
            f.write(report)
```

---

# 🚀 Step 2: Create Main Execution Script

Create:

```bash
nano reconcile.py
```

---

## reconcile.py

```python
#!/usr/bin/env python3

from transaction_parser import TransactionParser
from reconciliation_engine import ReconciliationEngine
from report_generator import ReportGenerator

def main():

    print(
        "Starting Payment Reconciliation..."
    )

    parser = TransactionParser()

    portal = parser.load_portal_transactions(
        "portal_transactions.csv"
    )

    bank = parser.load_bank_transactions(
        "bank_transactions.csv"
    )

    print(
        f"Portal Records: {len(portal)}"
    )

    print(
        f"Bank Records: {len(bank)}"
    )

    engine = ReconciliationEngine(
        portal,
        bank
    )

    results = engine.reconcile()

    print(
        f"Matches: {len(results['matched'])}"
    )

    print(
        f"Discrepancies: {len(results['discrepancies'])}"
    )

    report = ReportGenerator(results)

    report.save_report(
        "reconciliation_report.txt"
    )

    print(
        "Report Generated Successfully"
    )

if __name__ == "__main__":
    main()
```

---

# ▶️ Run Reconciliation

```bash
chmod +x reconcile.py

python3 reconcile.py
```

---

# ✅ Verification

---

## View Report

```bash
cat reconciliation_report.txt
```

Expected findings:

| Type           | Transaction |
| -------------- | ----------- |
| ✅ Match        | TXN001      |
| ✅ Match        | TXN002      |
| ✅ Match        | TXN003      |
| ✅ Match        | TXN006      |
| ⚠️ Discrepancy | TXN004      |
| ❌ Bank Only    | TXN007      |

---

## Verify Counts

```bash
python3 << EOF
from transaction_parser import TransactionParser
from reconciliation_engine import ReconciliationEngine

parser = TransactionParser()

portal = parser.load_portal_transactions(
'portal_transactions.csv'
)

bank = parser.load_bank_transactions(
'bank_transactions.csv'
)

engine = ReconciliationEngine(
portal,
bank
)

results = engine.reconcile()

print(
f"Matched: {len(results['matched'])}"
)

print(
f"Discrepancies: {len(results['discrepancies'])}"
)

print(
f"Portal only: {len(results['unmatched_portal'])}"
)

print(
f"Bank only: {len(results['unmatched_bank'])}"
)
EOF
```

Expected:

```text
Matched: 4
Discrepancies: 1
Portal only: 0
Bank only: 1
```

---

# 🧪 Edge Case Testing

Create:

```bash
nano test_edge_cases.py
```

```python
from transaction_parser import TransactionParser

parser = TransactionParser()

with open(
    "empty.csv",
    "w"
) as f:

    f.write(
        "transaction_id,date,amount,"
        "customer_id,status,payment_method\n"
    )

try:

    df = parser.load_portal_transactions(
        "empty.csv"
    )

    print(
        "PASS"
        if len(df) == 0
        else "FAIL"
    )

except Exception as e:

    print(
        f"FAIL - {e}"
    )
```

Run:

```bash
python3 test_edge_cases.py
```

---

# 🛠️ Troubleshooting

## ❌ Pandas Not Found

```bash
pip3 install pandas tabulate
```

Verify:

```bash
python3 -c \
"import pandas; print(pandas.__version__)"
```

---

## ❌ CSV Not Found

```bash
ls -la *.csv
```

Verify files exist.

---

## ❌ Floating Point Errors

Use:

```python
abs(a - b) < 0.01
```

instead of:

```python
a == b
```

---

## ❌ Empty DataFrame

Debug:

```python
print(df.head())
```

Verify column names match CSV headers.

---

# 🎯 Expected Outcomes

Upon completion:

✅ Transaction Parser

✅ Data Normalization

✅ Exact Match Detection

✅ Discrepancy Identification

✅ Missing Transaction Discovery

✅ Professional Audit Report

---

# 🌍 Real-World Applications

### 💳 Payment Gateway Reconciliation

Compare merchant portal records with bank settlements.

### 📊 Month-End Closing

Validate accounting transactions.

### 🚨 Fraud Detection

Identify suspicious mismatches.

### 🛡️ Financial Compliance

Generate audit-ready reports.

### 🏦 Enterprise FinTech Systems

Process millions of transactions daily.

---

# 🚀 Next Steps

### 📈 Dashboard Reporting

Integrate with Grafana or Power BI.

### ☁️ Cloud Storage

Store reports in S3.

### 📨 Automated Email Reports

Send reconciliation summaries.

### 🤖 Machine Learning

Detect anomaly patterns automatically.

### ⚡ Real-Time Reconciliation

Process streaming transactions.

---

# 🎉 Lab Completed Successfully

You have successfully built a payment reconciliation platform capable of:

💳 Parsing Financial Transactions

⚖️ Matching Records

🚨 Detecting Discrepancies

📊 Producing Audit Reports

🏦 Supporting Enterprise Financial Operations

This project demonstrates the core concepts used in production-grade FinTech reconciliation systems processing millions of transactions every day.

🚀 Happy Coding & Happy Reconciling!
