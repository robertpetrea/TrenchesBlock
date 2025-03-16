import argparse
import sys
from trenches import Trenches

class TrenchesCLI:
    def __init__(self):
        self.blockchain = Trenches(difficulty=4)
        self.parser = self.setup_parser()

    def setup_parser(self):
        parser = argparse.ArgumentParser(
            description='Trenches Blockchain CLI',
            usage='''trenches <command> [<args>]

Commands:
    add         Add a new transaction
    mine        Mine pending transactions
    show        Show the blockchain
    validate    Validate the blockchain
    difficulty  Change mining difficulty
''')
        parser.add_argument('command', help='Command to execute')
        return parser

    def add_transaction(self, args):
        if len(args) < 1:
            print("Usage: trenches add '<transaction_details>'")
            return
        transaction = ' '.join(args)
        self.blockchain.add_transaction(transaction)
        print(f"Transaction added: {transaction}")
        print(f"Pending transactions: {len(self.blockchain.pending_transactions)}")

    def mine(self, args):
        if len(args) < 1:
            print("Usage: trenches mine <miner_address>")
            return
        miner_address = args[0]
        print(f"Mining block... This may take a while.")
        self.blockchain.mine_pending_transactions(miner_address)
        print(f"Block mined! Miner: {miner_address}")

    def show_blockchain(self):
        print("\nBlockchain:")
        for block in self.blockchain.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")

    def validate_chain(self):
        is_valid = self.blockchain.is_chain_valid()
        print(f"\nBlockchain valid? {is_valid}")

    def set_difficulty(self, args):
        if len(args) < 1:
            print("Usage: trenches difficulty <number>")
            return
        try:
            difficulty = int(args[0])
            self.blockchain.difficulty = difficulty
            print(f"Mining difficulty set to {difficulty}")
        except ValueError:
            print("Please provide a valid number for difficulty")

    def run(self):
        args = self.parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Invalid command')
            self.parser.print_help()
            sys.exit(1)

        command = args.command
        command_args = sys.argv[2:]

        if command == 'add':
            self.add_transaction(command_args)
        elif command == 'mine':
            self.mine(command_args)
        elif command == 'show':
            self.show_blockchain()
        elif command == 'validate':
            self.validate_chain()
        elif command == 'difficulty':
            self.set_difficulty(command_args)

if __name__ == '__main__':
    TrenchesCLI().run() 