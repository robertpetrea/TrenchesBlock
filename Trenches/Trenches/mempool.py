from typing import List, Dict
from transaction import Transaction
import time

class Mempool:
    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.timestamp: Dict[str, float] = {}

    def add_transaction(self, transaction: Transaction) -> bool:
        """Add transaction to mempool"""
        tx_hash = transaction.calculate_hash()
        if tx_hash not in self.transactions:
            self.transactions[tx_hash] = transaction
            self.timestamp[tx_hash] = time.time()
            return True
        return False

    def remove_transaction(self, tx_hash: str) -> None:
        """Remove transaction from mempool"""
        if tx_hash in self.transactions:
            del self.transactions[tx_hash]
            del self.timestamp[tx_hash]

    def get_transactions(self, limit: int = None) -> List[Transaction]:
        """Get transactions sorted by fee/size ratio"""
        sorted_transactions = sorted(
            self.transactions.values(),
            key=lambda x: x.amount,  # Simple sorting by amount
            reverse=True
        )
        return sorted_transactions[:limit] if limit else sorted_transactions

    def clear_old_transactions(self, max_age: int = 72 * 3600) -> None:
        """Remove transactions older than max_age seconds"""
        current_time = time.time()
        old_transactions = [
            tx_hash for tx_hash, timestamp in self.timestamp.items()
            if current_time - timestamp > max_age
        ]
        for tx_hash in old_transactions:
            self.remove_transaction(tx_hash) 