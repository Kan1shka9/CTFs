#### computeAES

```
Encrypted with AES in ECB mode. All values base64 encoded
ciphertext = R9TacKHy6cf1AZho/nwWWYaNzP5GfltKE5yW+kwRYe0LY+PdGk1hfoanS/iVZ7z1
key = azdvtH4bvfdS/mryKLTNqQ==
```

`aes-decode.py`

```python
import base64
from Crypto.Cipher import AES

key = base64.b64decode("azdvtH4bvfdS/mryKLTNqQ==")
ciphertext = base64.b64decode("R9TacKHy6cf1AZho/nwWWYaNzP5GfltKE5yW+kwRYe0LY+PdGk1hfoanS/iVZ7z1")
crypter = AES.new(key, AES.MODE_ECB)
plaintext = crypter.decrypt(ciphertext).decode("utf-8")

print(plaintext)
```

```sh
u64@vm:~/Desktop$ sudo pip install pycrypto
```

```sh
u64@vm:~/Desktop$ python aes-decode.py
flag{do_not_let_machines_win_bdad81b3}__________
u64@vm:~/Desktop$
```