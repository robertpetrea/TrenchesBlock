import hashlib
import binascii
import random
from typing import Tuple
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class Wallet:
    def __init__(self):
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self._public_key = self._private_key.get_verifying_key()
        self.address = self.generate_address()
        self.balance = 0

    def generate_address(self) -> str:
        """Generate a wallet address from the public key"""
        public_key_bytes = self._public_key.to_string()
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        return 'TRX' + binascii.hexlify(ripemd160_hash).decode()[:34]

    def sign_transaction(self, transaction_data: str) -> bytes:
        """Sign a transaction with the private key"""
        return self._private_key.sign(transaction_data.encode())

    def get_public_key(self) -> str:
        """Get the public key in hex format"""
        return binascii.hexlify(self._public_key.to_string()).decode()

    @staticmethod
    def verify_signature(public_key: str, signature: bytes, transaction_data: str) -> bool:
        """Verify a transaction signature"""
        try:
            vk = VerifyingKey.from_string(
                binascii.unhexlify(public_key), 
                curve=SECP256k1
            )
            return vk.verify(signature, transaction_data.encode())
        except:
            return False 