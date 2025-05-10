from flask import Flask, request, jsonify, render_template
from blockchain import Blockchain
from wallet import Wallet
from transaction import Transaction

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain.chain)

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine_pending_transactions(miner_address="network")
    return jsonify({"message": "Block mined successfully!"})

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ['sender', 'recipient', 'amount', 'signature', 'public_key']

    if not all(field in tx_data for field in required_fields):
        return 'Missing fields', 400

    tx = Transaction(
        tx_data['sender'],
        tx_data['recipient'],
        tx_data['amount'],
        tx_data['signature'],
        tx_data['public_key']
    )

    if not tx.verify_signature():
        return 'Invalid signature', 400

    blockchain.add_transaction(tx)
    return 'Transaction added', 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
