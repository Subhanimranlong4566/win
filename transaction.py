import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

class Transaction:
    def __init__(self, sender, recipient, amount, signature, public_key):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature
        self.public_key = public_key

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def verify_signature(self):
        tx_data = json.dumps(self.to_dict(), sort_keys=True).encode()
        h = SHA256.new(tx_data)
        try:
            pub_key = RSA.import_key(self.public_key.encode())
            signature_bytes = base64.b64decode(self.signature)
            pkcs1_15.new(pub_key).verify(h, signature_bytes)
            return True
        except (ValueError, TypeError):
            return False
