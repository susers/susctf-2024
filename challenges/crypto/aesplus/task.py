from Crypto.Cipher import AES
import random
import secrets
import uuid

def aes_encrypt(key: bytes, data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)

def aes_decrypt(key: bytes, data: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

def aes_plus_encrypt(key: bytes, data: bytes) -> bytes:
    assert len(key) == 8
    keys = [
        b"SUSCTF-AESPLUS-0", b"SUSCTF-AESPLUS-1", b"SUSCTF-AESPLUS-2", b"SUSCTF-AESPLUS-3",
        b"SUSCTF-AESPLUS-4", b"SUSCTF-AESPLUS-5", b"SUSCTF-AESPLUS-6", b"SUSCTF-AESPLUS-7",
        b"SUSCTF-AESPLUS-8", b"SUSCTF-AESPLUS-9", b"SUSCTF-AESPLUS-a", b"SUSCTF-AESPLUS-b",
        b"SUSCTF-AESPLUS-c", b"SUSCTF-AESPLUS-d", b"SUSCTF-AESPLUS-e", b"SUSCTF-AESPLUS-f",
    ]
    random.seed(key[-3:])
    random.shuffle(keys)
    key_a = keys[key[0] >> 4]
    key_b = keys[key[0] % 16]
    key = int.from_bytes(key[1:-3], "big")
    for i in range(32):
        bit = (1 << i) & key
        if bit:
            data = aes_encrypt(key_a, data)
        else:
            data = aes_encrypt(key_b, data)
    return data

def aes_plus_decrypt(key: bytes, data: bytes) -> bytes:
    assert len(key) == 8
    keys = [
        b"SUSCTF-AESPLUS-0", b"SUSCTF-AESPLUS-1", b"SUSCTF-AESPLUS-2", b"SUSCTF-AESPLUS-3",
        b"SUSCTF-AESPLUS-4", b"SUSCTF-AESPLUS-5", b"SUSCTF-AESPLUS-6", b"SUSCTF-AESPLUS-7",
        b"SUSCTF-AESPLUS-8", b"SUSCTF-AESPLUS-9", b"SUSCTF-AESPLUS-a", b"SUSCTF-AESPLUS-b",
        b"SUSCTF-AESPLUS-c", b"SUSCTF-AESPLUS-d", b"SUSCTF-AESPLUS-e", b"SUSCTF-AESPLUS-f",
    ]
    random.seed(key[-3:])
    random.shuffle(keys)
    key_a = keys[key[0] >> 4]
    key_b = keys[key[0] % 16]
    key = int.from_bytes(key[1:-3], "big")
    for i in range(32-1, -1, -1):
        bit = (1 << i) & key
        if bit:
            data = aes_decrypt(key_a, data)
        else:
            data = aes_decrypt(key_b, data)
    return data

key = secrets.token_bytes(8)
plaintext = secrets.token_bytes(16)
ciphertext = aes_plus_encrypt(key, plaintext)
gift = plaintext.hex() + "|" + ciphertext.hex()
print(f"{gift = }")

flag = "---deleted---"
assert flag.startswith("susctf{") and flag.endswith("}")
assert len(flag) == 44
flag_uuid = uuid.UUID(flag[7:-1]).bytes
assert len(flag_uuid) == 16
assert str(uuid.UUID(bytes=flag_uuid)) == flag[7:-1]

c = aes_plus_encrypt(key, flag_uuid).hex()
print(f"{c = }")

"""
gift = 'd66fe087038cf381d3bcfe6bcf8c6a1b|6a0b644af7b11a267f8b97399e8bee39'
c = 'ba099276411c24b734948053cea63b4f'
"""
