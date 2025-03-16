import hashlib
import time
from typing import Any
from transaction import Transaction

class Block:
    def __init__(self, index: int, transactions: list[Transaction], previous_hash: str) -> None:
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self) -> str:
        """Calculate the Merkle root of transactions"""
        if not self.transactions:
            return hashlib.sha256("".encode()).hexdigest()
        
        transaction_hashes = [t.calculate_hash() for t in self.transactions]
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            transaction_hashes = [
                hashlib.sha256((h1 + h2).encode()).hexdigest()
                for h1, h2 in zip(transaction_hashes[::2], transaction_hashes[1::2])
            ]
        return transaction_hashes[0]

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block using SHA-256
        """
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            str(self.merkle_root) +
            str(self.previous_hash) +
            str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block by finding a hash that starts with the required number of zeros
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash() 