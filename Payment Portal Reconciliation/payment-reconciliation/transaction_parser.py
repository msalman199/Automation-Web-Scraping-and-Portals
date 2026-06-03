import pandas as pd
from typing import Dict, List

class TransactionParser:
    """
    Parse and normalize transaction records from different sources.
    """
    
    def __init__(self):
        self.portal_data = None
        self.bank_data = None
    
    def load_portal_transactions(self, filepath: str) -> pd.DataFrame:
        """
        Load and normalize portal transaction data.
        
        Args:
            filepath: Path to portal transactions CSV
            
        Returns:
            Normalized DataFrame with standard column names
        """
        # TODO: Read CSV file using pandas
        # TODO: Filter only 'completed' status transactions
        # TODO: Rename columns to standard format (id, date, amount, customer)
        # TODO: Convert amount to float
        # TODO: Return normalized DataFrame
        pass
    
    def load_bank_transactions(self, filepath: str) -> pd.DataFrame:
        """
        Load and normalize bank transaction data.
        
        Args:
            filepath: Path to bank transactions CSV
            
        Returns:
            Normalized DataFrame with standard column names
        """
        # TODO: Read CSV file using pandas
        # TODO: Rename columns to match portal format
        # TODO: Convert amount to float
        # TODO: Return normalized DataFrame
        pass
    
    def get_transaction_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for transactions.
        
        Args:
            df: Transaction DataFrame
            
        Returns:
            Dictionary with count, total_amount, avg_amount
        """
        # TODO: Calculate total count of transactions
        # TODO: Calculate sum of all amounts
        # TODO: Calculate average amount
        # TODO: Return dictionary with statistics
        pass
