import secrets
from utils import nbit, LFSR, NFSR

def proof_of_work():
    import string, hashlib, random

    alphabet = string.ascii_letters + string.digits
    proof = ''.join(random.choices(alphabet, k=16))
    digest = hashlib.sha256(proof.encode()).hexdigest()

    print(f"sha256(XXXX+{proof[4:]})=={digest}")
    x = input("Give me XXXX:")
    h = hashlib.sha256((x + proof[4:]).encode()).hexdigest()
    return h == digest

assert proof_of_work()
print("Good luck")
try:
    for i in range(5):
        seeds = [secrets.randbits(nbit) for _ in range(2)]
        masks = [secrets.randbits(nbit) for _ in range(2)]
        lfsrs = [LFSR(seed, mask) for seed, mask in zip(seeds, masks)]
        nfsr = NFSR(*lfsrs)

        msg = secrets.token_bytes(200)
        enc = nfsr(msg)

        print(f"Round {i+1}: {enc.hex()}")
        print(f"{masks = }")
        if not bytes.fromhex(input('>')) == msg:
            raise Exception
    flag = open('/flag', 'r').read()
    print(f"Congratulations: {flag}")
except:
    print("Not this time")