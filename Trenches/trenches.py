from typing import List, Any
from block import Block

class Trenches:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Any] = []
        
        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        Create the first block in the blockchain
        """
        genesis_block = Block(0, ["Genesis Block"], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """
        Return the most recent block in the chain
        """
        return self.chain[-1]

    def add_transaction(self, transaction: Any) -> None:
        """
        Add a new transaction to pending transactions
        """
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str) -> None:
        """
        Create a new block with all pending transactions and mine it
        """
        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        # Clear pending transactions and reward the miner
        self.pending_transactions = [
            f"Mining Reward: {10} coins to {miner_address}"
        ]

    def is_chain_valid(self) -> bool:
        """
        Verify the blockchain's integrity
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False

        return True 