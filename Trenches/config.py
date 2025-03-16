from dataclasses import dataclass

@dataclass
class BlockchainConfig:
    DIFFICULTY: int = 4
    MINING_REWARD: float = 10.0
    BLOCK_TIME: int = 600  # Target 10 minutes like Bitcoin
    DIFFICULTY_ADJUSTMENT_INTERVAL: int = 2016  # Blocks
    MAX_TRANSACTIONS_PER_BLOCK: int = 1000
    MINIMUM_TRANSACTION_AMOUNT: float = 0.00001
    NETWORK_PORT: int = 5000
    VERSION: str = "1.0.0" 