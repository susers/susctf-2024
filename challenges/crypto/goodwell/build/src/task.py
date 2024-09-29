from Crypto.Cipher import AES
import secrets

key = secrets.token_bytes(16)
seed = secrets.randbits(128)

def safe_random():
    global seed
    seed = seed << 16 | seed >> 112
    seed ^= seed >> 92
    seed &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    return seed

def encrypt(data, nonce=None):
    if not nonce:
        nonce = safe_random().to_bytes(16, "big")
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    return nonce + cipher.encrypt(data) + cipher.digest()

def decrypt(data):
    cipher = AES.new(key, AES.MODE_GCM, data[:16])
    return cipher.decrypt_and_verify(data[16:-16], data[-16:])

times = 0
def blab():
    global times
    times += 1
    if times == 1:
        return "nice to meet you"
    elif times == 2:
        return "nice to meet you too"
    else:
        return f"nice to meet you {times}"

while True:
    word = input("say something: ")
    try:
        assert len(word) < 1024
        implication = decrypt(bytes.fromhex(word))
        if implication == b"flag":
            flag = open("/flag", "r").read().strip()
            reply = f"Here is the flag: {flag}"
        else:
            reply = f"I know what you said: {implication.decode()}"
    except:
        reply = blab()
    reply = encrypt(reply.encode())
    print(reply.hex())
