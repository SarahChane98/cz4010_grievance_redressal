import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

# random_generator = Random.new().read
# key = RSA.generate(1024, random_generator)  # generate pub and private key
# pub_key = key.publickey().exportKey().decode('utf-8')
# print(pub_key)
# padded_key = pad(bytes("password", 'utf-8'), 16)
# cipher = AES.new(padded_key, AES.MODE_EAX, b'0')
# pri_key = cipher.encrypt(key.exportKey())
# print(pri_key)
# str_key = str(pri_key, encoding='ASCII')
# # print(type(str_key))
# bytes_key = bytearray(str_key, encoding='ASCII')
# print(bytes_key)

str_pub = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC6GCCs5EX0u8w7J3GXiS9jajUU
z2Cz86TRF6qw4GKUl17o83qzf51ux/+abiLhR1cZQHI5iPxpcBzxN+BMHS7LzMfi
Q5XwuQtAhM6/hdimYXb0YGDUrN4cG8arShdhYY0GQPHI0nbl3283pHh2oCHpLTC2
nWD7nbN6T2OSm8hcsQIDAQAB
-----END PUBLIC KEY-----"""

key = RSA.importKey(str_pub)
# print(AES.new(padded_key, AES.MODE_EAX, user.nonce).decrypt(user.pri_key).decode("utf-8"))
