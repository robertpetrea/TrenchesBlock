import hashlib
import time
from typing import Optional, Tuple

class ProofOfWork:
    def __init__(self, block_data: str, difficulty: int):
        self.block_data = block_data
        self.difficulty = difficulty
        self.target = "0" * difficulty
        
    def compute(self, max_nonce: int = 1000000) -> Tuple[int, str]:
        """Compute proof of work"""
        for nonce in range(max_nonce):
            hash_attempt = self.calculate_hash(nonce)
            if hash_attempt.startswith(self.target):
                return nonce, hash_attempt
        return -1, ""
        
    def calculate_hash(self, nonce: int) -> str:
        """Calculate hash with nonce"""
        data = f"{self.block_data}{nonce}"
        return hashlib.sha256(data.encode()).hexdigest()
        
    @staticmethod
    def verify(block_data: str, nonce: int, difficulty: int) -> bool:
        """Verify proof of work"""
        hash_result = hashlib.sha256(f"{block_data}{nonce}".encode()).hexdigest()
        return hash_result.startswith("0" * difficulty)

class DifficultyAdjuster:
    def __init__(self, target_block_time: int, adjustment_factor: float = 0.25):
        self.target_block_time = target_block_time
        self.adjustment_factor = adjustment_factor
        
    def adjust_difficulty(self, current_difficulty: int, 
                         last_block_time: float, 
                         current_block_time: float) -> int:
        """Adjust mining difficulty based on block time"""
        time_taken = current_block_time - last_block_time
        
        if time_taken < self.target_block_time / 2:
            return current_difficulty + 1
        elif time_taken > self.target_block_time * 2:
            return max(1, current_difficulty - 1)
            
        return current_difficulty 