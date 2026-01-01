#!pip install pycryptodome

import binascii
import datetime
import collections
import Crypto
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

class Transaction:
    def __init__ (self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.receiver,
            'value': self.amount,
            'time': self.time })

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""

    last_block_hash=""

def display_transaction(transaction):
    dict = transaction.to_dict()
    print ("Sender: " +dict['sender'])
    print('------')
    print ("Receiver: " +dict['recipient'])
    print('------')
    print ("Amount: " +str(dict['value']))
    print('------')
    print ("Time: " +str(dict['time']))
    print('------')
        
transactions = []

Bhavesh = Client()
Prabal = Client()
Laxmikant = Client()
Umesh = Client()

t1= Transaction(Prabal, Bhavesh.identity, 2.0)
t1.sign_transaction()
transactions.append(t1)

t2= Transaction(Bhavesh, Umesh.identity, 1.0)
t2.sign_transaction()
transactions.append(t2)

t3= Transaction(Laxmikant, Bhavesh.identity, 2.0)
t3.sign_transaction()
transactions.append(t3)

t4= Transaction(Bhavesh, Prabal.identity, 1.0)
t4.sign_transaction()
transactions.append(t4)

t5= Transaction(Umesh, Laxmikant.identity, 2.0)
t5.sign_transaction()
transactions.append(t5)

for trans in transactions:
    display_transaction(trans)
    print("#################################")



