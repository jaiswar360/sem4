import rsa

publicKey, privateKey = rsa.newkeys(512)

message = "Hello World"

encMsg = rsa.encrypt(message.encode(),publicKey)

print("Original Message:",message)
print("Encrypted message:",encMsg)

decMsg = rsa.decrypt(encMsg,privateKey).decode()

print("Decrypted Message:", decMsg)

