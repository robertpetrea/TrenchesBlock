import logging
from datetime import datetime
import os

class BlockchainLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Set up logging
        self.logger = logging.getLogger('TrenchesBlockchain')
        self.logger.setLevel(logging.INFO)

        # Create file handler
        fh = logging.FileHandler(f'logs/blockchain_{datetime.now().strftime("%Y%m%d")}.log')
        fh.setLevel(logging.INFO)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def log_transaction(self, transaction):
        self.logger.info(f"New transaction: {transaction.sender} -> {transaction.recipient}: {transaction.amount}")

    def log_block_mined(self, block):
        self.logger.info(f"Block mined: #{block.index} with {len(block.transactions)} transactions")

    def log_error(self, error):
        self.logger.error(f"Error: {str(error)}") 