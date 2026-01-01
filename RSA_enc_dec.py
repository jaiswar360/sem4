# !pip install pycryptodome

import binascii
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# -------- Client Class --------
class Client:
    def __init__(self, name):
        self.name = name
        random_generator = Random.new().read
        self.private_key = RSA.generate(1024, random_generator)
        self.public_key = self.private_key.publickey()

    @property
    def identity(self):
        return binascii.hexlify(self.public_key.exportKey(format='DER')).decode('ascii')

    def encrypt_message(self, message, receiver_public_key):
        cipher = PKCS1_OAEP.new(receiver_public_key)
        encrypted_msg = cipher.encrypt(message.encode())
        return encrypted_msg

    def decrypt_message(self, encrypted_msg):
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_msg = cipher.decrypt(encrypted_msg)
        return decrypted_msg.decode()


# -------- Demo: Two Users --------
sender = Client("kamal")
receiver = Client("amit")

print("Sender Identity:", sender.identity)
print("Receiver Identity:", receiver.identity)

# Message
message = "Hello amit, this is a secure message!"

# Sender encrypts using Receiver's PUBLIC key
encrypted_message = sender.encrypt_message(message, receiver.public_key)
print("\nEncrypted Message (ciphertext):", encrypted_message)

# Receiver decrypts using his PRIVATE key
decrypted_message = receiver.decrypt_message(encrypted_message)
print("\nDecrypted Message (plain text):", decrypted_message)

