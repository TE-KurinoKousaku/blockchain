# coding: UTF-8

import json
import hashlib
from time import time
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self, network_id=1, genesis='./genesis.json'):
        genesis_block = json.load(open(genesis, 'r'))

        self.network_id = network_id
        self.chain = [genesis_block]
        self.current_transactions = {}
        self.difficulty = genesis_block['difficulty']

    def proof_of_work(self, last_nonce):
        nonce = 0

        while self.valid_proof(last_nonce, nonce) is False:
            nonce += 1

        return nonce

    def valid_proof(self, last_nonce, nonce):

        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:self.difficulty] == '0' * self.difficulty


    def new_block(self, nonce, previous_hash=None):
        block = {
            'network_id': self.network_id,
            'difficulty': self.difficulty,
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash(self.last_block),
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

if __name__ == '__main__':
    bc = Blockchain()
    last_nonce = bc.last_block['nonce']
    nonce = bc.proof_of_work(last_nonce)
    print(nonce)
    bc.new_block(nonce)
    print(bc.last_block)