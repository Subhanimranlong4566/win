from block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address):
        from transaction import Transaction
        reward_tx = Transaction("Network", miner_address, self.mining_reward, "", "")
        self.pending_transactions.append(reward_tx)
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_last_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
