import time
from typing import Dict, Any, List
from dataclasses import dataclass
import hashlib

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    timestamp: float
    fee: float = 0.001
    signature: bytes = None
    transaction_id: str = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'fee': self.fee,
            'signature': self.signature.hex() if self.signature else None,
            'transaction_id': self.transaction_id
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Transaction':
        return Transaction(
            sender=data['sender'],
            recipient=data['recipient'],
            amount=data['amount'],
            timestamp=data['timestamp'],
            fee=data['fee'],
            signature=bytes.fromhex(data['signature']) if data['signature'] else None,
            transaction_id=data['transaction_id']
        )

    def calculate_hash(self) -> str:
        """Calculate unique transaction hash"""
        transaction_string = (
            f"{self.sender}{self.recipient}{self.amount}{self.timestamp}{self.fee}"
        )
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def calculate_total(self) -> float:
        """Calculate total amount including fee"""
        return self.amount + self.fee

class MerkleTree:
    @staticmethod
    def create_merkle_root(transactions: List['Transaction']) -> str:
        """Create Merkle root from transactions"""
        if not transactions:
            return hashlib.sha256("".encode()).hexdigest()
            
        transaction_hashes = [tx.calculate_hash() for tx in transactions]
        
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
                
            new_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                combined = transaction_hashes[i] + transaction_hashes[i+1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            transaction_hashes = new_hashes
            
        return transaction_hashes[0] 