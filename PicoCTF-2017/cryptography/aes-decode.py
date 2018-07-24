import base64
from Crypto.Cipher import AES

key = base64.b64decode("azdvtH4bvfdS/mryKLTNqQ==")
ciphertext = base64.b64decode("R9TacKHy6cf1AZho/nwWWYaNzP5GfltKE5yW+kwRYe0LY+PdGk1hfoanS/iVZ7z1")
crypter = AES.new(key, AES.MODE_ECB)
plaintext = crypter.decrypt(ciphertext).decode("utf-8")

print(plaintext)
