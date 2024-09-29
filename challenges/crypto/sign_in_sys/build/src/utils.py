from Crypto.Util.number import *
from random import getrandbits

class SISystem:
    def __init__(self, nbits: int):
        self.nbits = nbits
        self.store = set()
        self.setup()
        self.gen()
    
    def __str__(self):
        return f"{self.param = }"
        
    def setup(self):
        while True:
            q, r = getPrime(self.nbits>>1), getPrime(self.nbits>>1)
            p = 2*r*q + 1
            if isPrime(p): break
        while True:
            g = getrandbits(self.nbits) % p
            if pow(g, 2*r, p) != 1:
                g = pow(g, 2*r, p)
                break
        t = getrandbits(self.nbits>>1) % q
        self.param = (p, q, g, t)
    
    def gen(self):
        p, q, g, _ = self.param
        self.sk = getrandbits(self.nbits>>1) % q
        self.pk = pow(g, self.sk, p)
        self.salt = long_to_bytes(getrandbits(32), 4)

    def check(self, m: bytes):
        assert len(m) <= 128 and max(list(m)) <= 128 and m not in self.store

    def H(self, m: bytes):
        _, q, _, t = self.param
        h = 0
        for mi in m + self.salt:
            h = (h ^ mi) * t % q
        return h

    def sign(self, m_hex):
        m = bytes.fromhex(m_hex)
        self.check(m)
        self.store.add(m)

        p, q, g, _ = self.param
        k = getrandbits(self.nbits>>1) % q
        r = pow(g, k, p)
        s = inverse(k, q)*(self.H(m) + self.sk*r) % q
        return r, s

    def verify(self, m_hex, sig):
        m = bytes.fromhex(m_hex)
        self.check(m)

        p, q, g, _ = self.param
        r, s = sig
        w = inverse(s, q)
        u1 = self.H(m)*w % q
        u2 = r*w % q
        v = pow(g, u1, p)*pow(self.pk, u2, p) % p
        return v == r