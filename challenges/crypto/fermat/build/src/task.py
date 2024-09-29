import hashlib, random, string
from Crypto.Util.number import getPrime

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

p, q = 3, 3
while p % 4 == 3:
    p = getPrime(512)
while q % 4 == 3:
    q = getPrime(512)

n = p*q
gift = p**3 + q**3

print(f"n = {n}")
print(f"gift = {gift}")

try:
    a = int(input("a = "))
    b = int(input("b = "))
    assert a > 0 and b > 0
except:
    print("Invalid input")
    exit()

if a**2 + b**2 == n:
    flag = open("/flag", "r").read().strip()
    print(f"Here is your flag: {flag}")
else:
    print("Wrong!")
