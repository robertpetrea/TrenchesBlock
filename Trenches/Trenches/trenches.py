from typing import List, Dict, Any
from block import Block
from transaction import Transaction
from wallet import Wallet
from config import BlockchainConfig
import time

class Trenches:
    def __init__(self, difficulty: int = BlockchainConfig.DIFFICULTY):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.wallets: Dict[str, float] = {}  # address -> balance
        self.config = BlockchainConfig()
        
        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        Create the first block in the blockchain
        """
        genesis_transaction = Transaction(
            "0",  # Genesis address
            "0",  # Genesis address
            0,    # Amount
            time.time()
        )
        genesis_block = Block(0, [genesis_transaction], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """
        Return the most recent block in the chain
        """
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a new transaction to pending transactions
        """
        # Verify transaction
        if not self._verify_transaction(transaction):
            return False
            
        # Check minimum amount
        if transaction.amount < self.config.MINIMUM_TRANSACTION_AMOUNT:
            return False

        # Check if sender has enough balance
        if not self._has_sufficient_balance(transaction):
            return False

        self.pending_transactions.append(transaction)
        return True

    def _verify_transaction(self, transaction: Transaction) -> bool:
        """
        Verify transaction signature and validity
        """
        if transaction.sender == "0":  # Genesis transaction
            return True
            
        try:
            # Verify signature
            transaction_data = f"{transaction.sender}{transaction.recipient}{transaction.amount}{transaction.timestamp}"
            return Wallet.verify_signature(
                transaction.sender,  # Using address as public key
                transaction.signature,
                transaction_data
            )
        except:
            return False

    def _has_sufficient_balance(self, transaction: Transaction) -> bool:
        """
        Check if sender has sufficient balance
        """
        if transaction.sender == "0":  # Genesis or mining reward
            return True
            
        sender_balance = self.get_balance(transaction.sender)
        return sender_balance >= transaction.amount

    def get_balance(self, address: str) -> float:
        """
        Calculate balance for an address
        """
        balance = 0.0
        
        # Go through all blocks
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
                    
        return balance

    def mine_pending_transactions(self, miner_address: str) -> bool:
        """
        Create a new block with pending transactions and mine it
        """
        # Check max transactions per block
        transactions_to_mine = self.pending_transactions[:self.config.MAX_TRANSACTIONS_PER_BLOCK]
        
        block = Block(
            len(self.chain),
            transactions_to_mine,
            self.get_latest_block().hash
        )
        
        try:
            block.mine_block(self.difficulty)
            self.chain.append(block)
            
            # Remove mined transactions from pending
            self.pending_transactions = self.pending_transactions[self.config.MAX_TRANSACTIONS_PER_BLOCK:]
            
            # Add mining reward
            reward_transaction = Transaction(
                "0",  # Mining rewards come from network
                miner_address,
                self.config.MINING_REWARD,
                time.time()
            )
            self.pending_transactions.append(reward_transaction)
            
            return True
        except Exception as e:
            print(f"Mining failed: {e}")
            return False

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

            # Verify all transactions in block
            for transaction in current_block.transactions:
                if not self._verify_transaction(transaction):
                    return False

        return True

    def adjust_difficulty(self) -> None:
        """
        Adjust mining difficulty based on block time
        """
        if len(self.chain) % self.config.DIFFICULTY_ADJUSTMENT_INTERVAL != 0:
            return

        expected_time = self.config.BLOCK_TIME * self.config.DIFFICULTY_ADJUSTMENT_INTERVAL
        actual_time = self.chain[-1].timestamp - self.chain[-self.config.DIFFICULTY_ADJUSTMENT_INTERVAL].timestamp

        if actual_time < expected_time / 2:
            self.difficulty += 1
        elif actual_time > expected_time * 2:
            self.difficulty = max(1, self.difficulty - 1) 