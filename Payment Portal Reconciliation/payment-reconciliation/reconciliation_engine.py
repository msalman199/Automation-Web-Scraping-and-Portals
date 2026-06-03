import pandas as pd
from typing import Tuple, List, Dict

class ReconciliationEngine:
    """
    Match transactions between portal and bank records.
    """
    
    def __init__(self, portal_df: pd.DataFrame, bank_df: pd.DataFrame):
        self.portal_df = portal_df
        self.bank_df = bank_df
        self.matched = []
        self.unmatched_portal = []
        self.unmatched_bank = []
        self.discrepancies = []
    
    def find_exact_matches(self) -> List[Dict]:
        """
        Find transactions that match exactly on ID and amount.
        
        Returns:
            List of matched transaction dictionaries
        """
        # TODO: Merge DataFrames on transaction ID
        # TODO: Compare amounts (consider floating point precision)
        # TODO: Identify exact matches where amounts are equal
        # TODO: Store matched records
        # TODO: Return list of matches
        pass
    
    def find_amount_discrepancies(self, tolerance: float = 0.01) -> List[Dict]:
        """
        Find transactions with matching IDs but different amounts.
        
        Args:
            tolerance: Acceptable difference threshold
            
        Returns:
            List of discrepancy dictionaries with both amounts
        """
        # TODO: Merge DataFrames on transaction ID
        # TODO: Find records where amounts differ by more than tolerance
        # TODO: Create discrepancy records with portal_amount and bank_amount
        # TODO: Return list of discrepancies
        pass
    
    def find_unmatched_transactions(self) -> Tuple[List[str], List[str]]:
        """
        Identify transactions present in only one source.
        
        Returns:
            Tuple of (portal_only_ids, bank_only_ids)
        """
        # TODO: Get set of portal transaction IDs
        # TODO: Get set of bank transaction IDs
        # TODO: Find IDs in portal but not in bank
        # TODO: Find IDs in bank but not in portal
        # TODO: Return both lists as tuple
        pass
    
    def reconcile(self) -> Dict:
        """
        Perform complete reconciliation process.
        
        Returns:
            Dictionary with all reconciliation results
        """
        # TODO: Call find_exact_matches()
        # TODO: Call find_amount_discrepancies()
        # TODO: Call find_unmatched_transactions()
        # TODO: Compile results into summary dictionary
        # TODO: Return complete reconciliation report
        pas
