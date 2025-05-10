from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import json

class Wallet:
    def __init__(self):
        self.key_pair = RSA.generate(2048)
        self.private_key = self.key_pair.export_key()
        self.public_key = self.key_pair.publickey().export_key()

    def sign_transaction(self, transaction_data):
        h = SHA256.new(json.dumps(transaction_data, sort_keys=True).encode())
        signature = pkcs1_15.new(self.key_pair).sign(h)
        return base64.b64encode(signature).decode()

    def get_public_key(self):
        return self.public_key.decode()
