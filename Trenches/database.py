import sqlite3
from typing import List, Optional
from block import Block
from transaction import Transaction

class BlockchainDB:
    def __init__(self, db_file: str = "blockchain.db"):
        self.db_file = db_file
        self._create_tables()

    def _create_tables(self) -> None:
        """Create necessary database tables"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Create blocks table
        c.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                height INTEGER PRIMARY KEY,
                timestamp REAL,
                previous_hash TEXT,
                hash TEXT,
                nonce INTEGER,
                merkle_root TEXT
            )
        ''')
        
        # Create transactions table
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                tx_hash TEXT PRIMARY KEY,
                block_height INTEGER,
                sender TEXT,
                recipient TEXT,
                amount REAL,
                timestamp REAL,
                signature TEXT,
                FOREIGN KEY (block_height) REFERENCES blocks(height)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_block(self, block: Block) -> None:
        """Save block to database"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Save block
        c.execute('''
            INSERT INTO blocks VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            block.index,
            block.timestamp,
            block.previous_hash,
            block.hash,
            block.nonce,
            block.merkle_root
        ))
        
        # Save transactions
        for tx in block.transactions:
            c.execute('''
                INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                tx.calculate_hash(),
                block.index,
                tx.sender,
                tx.recipient,
                tx.amount,
                tx.timestamp,
                tx.signature.hex() if tx.signature else None
            ))
        
        conn.commit()
        conn.close()

    def get_block(self, height: int) -> Optional[Block]:
        """Retrieve block from database"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Get block
        c.execute('SELECT * FROM blocks WHERE height = ?', (height,))
        block_data = c.fetchone()
        
        if not block_data:
            return None
            
        # Get transactions for this block
        c.execute('SELECT * FROM transactions WHERE block_height = ?', (height,))
        tx_data = c.fetchall()
        
        transactions = [
            Transaction(
                sender=tx[2],
                recipient=tx[3],
                amount=tx[4],
                timestamp=tx[5],
                signature=bytes.fromhex(tx[6]) if tx[6] else None
            ) for tx in tx_data
        ]
        
        # Reconstruct block
        block = Block(
            index=block_data[0],
            transactions=transactions,
            previous_hash=block_data[2]
        )
        block.timestamp = block_data[1]
        block.hash = block_data[3]
        block.nonce = block_data[4]
        
        conn.close()
        return block 