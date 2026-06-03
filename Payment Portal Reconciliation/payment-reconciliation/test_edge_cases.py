from transaction_parser import TransactionParser
from reconciliation_engine import ReconciliationEngine

# Test with empty files
parser = TransactionParser()

# Create empty test file
with open('empty.csv', 'w') as f:
    f.write('transaction_id,date,amount,customer_id,status,payment_method\n')

try:
    df = parser.load_portal_transactions('empty.csv')
    print(f"Empty file handling: {'PASS' if len(df) == 0 else 'FAIL'}")
except Exception as e:
    print(f"Empty file handling: FAIL - {e}")
