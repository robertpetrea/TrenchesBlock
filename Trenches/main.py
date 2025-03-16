from trenches import Trenches

def main():
    # Create new blockchain
    trenches = Trenches(difficulty=4)
    
    print("Mining genesis block...")
    
    # Add some transactions
    trenches.add_transaction("Alice sends 10 coins to Bob")
    trenches.add_transaction("Bob sends 5 coins to Charlie")
    
    print("Mining first block...")
    trenches.mine_pending_transactions("miner1")
    
    # Add more transactions
    trenches.add_transaction("Charlie sends 3 coins to David")
    trenches.add_transaction("David sends 1 coin to Alice")
    
    print("Mining second block...")
    trenches.mine_pending_transactions("miner2")
    
    # Verify the blockchain
    print(f"\nBlockchain valid? {trenches.is_chain_valid()}")
    
    # Print the blockchain
    print("\nBlockchain:")
    for block in trenches.chain:
        print(f"\nBlock #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Transactions: {block.transactions}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print(f"Nonce: {block.nonce}")

if __name__ == "__main__":
    main() 