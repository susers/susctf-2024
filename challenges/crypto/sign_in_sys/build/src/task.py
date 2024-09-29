from utils import SISystem
import secrets

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
sus = secrets.token_hex(64).encode()
sus_hex = sus.hex()
sisys = SISystem(nbits=256)
print(sisys)

MENU = '''
= SignInSystem =
[S]ign
[V]erify
[H]int'''
for _ in range(5):
    try:
        print(MENU)
        choice = input('>').lower()

        if choice == 's':
            m_hex = input("m_hex>")
            if m_hex == sus_hex:
                print("Nah")
            else:
                print(f"{sisys.sign(m_hex=m_hex) = }")

        if choice == 'v':
            m_hex = input("m_hex>")
            r, s = int(input("r>")), int(input("s>"))
            if sisys.verify(m_hex=sus_hex, sig=(r, s)):
                flag = open('/flag', 'r').read()
                print(f"Congratulations: {flag}")
            else:
                print(f"{sisys.verify(m_hex=m_hex, sig=(r, s)) = }")

        if choice == 'h':
            pk = int(input("pk>"))
            if pk == sisys.pk:
                print(f"{sus_hex = }")
    except:
        break
