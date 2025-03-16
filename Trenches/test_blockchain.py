import unittest
from trenches import Trenches
from wallet import Wallet
from transaction import Transaction
import time

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Trenches(difficulty=2)  # Lower difficulty for testing
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()

    def test_create_wallet(self):
        self.assertIsNotNone(self.wallet1.address)
        self.assertTrue(self.wallet1.address.startswith('TRX'))

    def test_create_transaction(self):
        transaction = Transaction(
            self.wallet1.address,
            self.wallet2.address,
            10.0,
            time.time()
        )
        self.assertIsNotNone(transaction)

    def test_mine_block(self):
        result = self.blockchain.mine_pending_transactions(self.wallet1.address)
        self.assertTrue(result)
        self.assertEqual(len(self.blockchain.chain), 2)  # Genesis block + 1

if __name__ == '__main__':
    unittest.main() 