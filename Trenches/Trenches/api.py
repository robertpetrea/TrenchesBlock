from flask import Flask, jsonify, request
from trenches import Trenches
from wallet import Wallet
from transaction import Transaction
import time
from mempool import Mempool
from database import BlockchainDB
from smart_contract import SmartContract
from network import P2PNode

app = Flask(__name__)
blockchain = Trenches()

# Initialize components
mempool = Mempool()
db = BlockchainDB()
p2p_node = P2PNode()

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    wallet = Wallet()
    return jsonify({
        'address': wallet.address,
        'public_key': wallet.get_public_key(),
        'private_key': wallet._private_key.to_string().hex()
    })

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = Transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount'],
        timestamp=time.time(),
        signature=bytes.fromhex(values['signature'])
    )
    
    blockchain.add_transaction(transaction)
    return jsonify({'message': 'Transaction added successfully'})

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [vars(block) for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response)

@app.route('/mempool', methods=['GET'])
def get_mempool():
    """Get all transactions in mempool"""
    transactions = mempool.get_transactions()
    return jsonify([tx.to_dict() for tx in transactions])

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Get balance for an address"""
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance})

@app.route('/block/<int:height>', methods=['GET'])
def get_block(height):
    """Get block by height"""
    block = db.get_block(height)
    if block:
        return jsonify(vars(block))
    return 'Block not found', 404

@app.route('/mine', methods=['POST'])
def mine():
    """Mine a new block"""
    values = request.get_json()
    if not values.get('miner_address'):
        return 'Missing miner_address', 400
        
    success = blockchain.mine_pending_transactions(values['miner_address'])
    if success:
        # Save to database
        db.save_block(blockchain.get_latest_block())
        return jsonify({'message': 'Block mined successfully'})
    return 'Mining failed', 500

@app.route('/contract/deploy', methods=['POST'])
def deploy_contract():
    """Deploy a smart contract"""
    values = request.get_json()
    if not values.get('code') or not values.get('initial_state'):
        return 'Missing values', 400
        
    contract = SmartContract(values['code'], values['initial_state'])
    # Add contract to blockchain
    return jsonify({'contract_address': contract.contract_address})

@app.route('/contract/execute', methods=['POST'])
def execute_contract():
    """Execute a smart contract function"""
    values = request.get_json()
    if not all(k in values for k in ['contract_address', 'function', 'args']):
        return 'Missing values', 400
        
    # Execute contract function
    result = blockchain.execute_contract(
        values['contract_address'],
        values['function'],
        values['args']
    )
    return jsonify({'result': result})

@app.route('/peers', methods=['GET'])
def get_peers():
    """Get list of peers"""
    return jsonify({'peers': list(p2p_node.peers)})

@app.route('/peers/add', methods=['POST'])
def add_peer():
    """Add a new peer"""
    values = request.get_json()
    if not values.get('peer'):
        return 'Missing peer address', 400
        
    p2p_node.peers.add(values['peer'])
    return jsonify({'message': 'Peer added successfully'})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get blockchain statistics"""
    return jsonify({
        'blocks': len(blockchain.chain),
        'transactions': sum(len(block.transactions) for block in blockchain.chain),
        'difficulty': blockchain.difficulty,
        'peers': len(p2p_node.peers)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 