import hashlib, random, string
from Crypto.Util.number import bytes_to_long, isPrime

def proof_of_work():
    alphabet = string.ascii_letters + string.digits
    proof = ''.join(random.choices(alphabet, k=16))
    digest = hashlib.sha256(proof.encode()).hexdigest()
    print(f"sha256(XXXX+{proof[4:]})=={digest}")
    x = input("Give me XXXX:")
    h = hashlib.sha256((x + proof[4:]).encode()).hexdigest()
    return h == digest

if not proof_of_work():
    print("Do proof of work first!")
    exit()

target = bytes_to_long(b"# susctf crypto challenge #")

def fibonacci(i, p):
    if i <= 0: return 0
    mul = lambda a, b: [
        (a[0] * b[0] + a[1] * b[1]) % p,
        (a[0] * b[1] + a[1] * b[2]) % p,
        (a[1] * b[1] + a[2] * b[2]) % p
    ]
    F = [1, 1, 0]
    C = [1, 0, 1]
    while i > 0:
        if i & 1:
            C = mul(C, F)
        F = mul(F, F)
        i >>= 1
    return C[1]

index = int(input("index: "))
prime = int(input("prime: "))

if not (isPrime(prime) and prime.bit_length() == 256):
    print("Invalid prime")
    exit()
if index < 0 or index.bit_length() > 256:
    print("Invalid index")
    exit()
if fibonacci(index, prime) == target:
    flag = open("/flag", "r").read().strip()
    print(flag)
else:
    print("Wrong!")
