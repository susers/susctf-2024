nbit = 128

class LFSR:
    def __init__(self, seed: int, mask: int):
        self.state = seed & (2**nbit - 1)
        self.mask = mask & (2**nbit - 1)

    def __next__(self):
        out = (self.state & self.mask).bit_count() & 1
        self.state = ((self.state << 1) | out) & (2**nbit - 1)
        return out
    
    def __call__(self, bits: int):
        out = 0
        for _ in range(bits):
            out = (out << 1) | next(self)
        return out

class NFSR:
    def __init__(self, lfsr0: LFSR, lfsr1: LFSR):
        self.lfsr0 = lfsr0
        self.lfsr1 = lfsr1
    
    def __call__(self, msg: bytes):
        enc = list()
        for m in msg:
            if self.lfsr0(1):
                enc += [m & self.lfsr1(8), m | self.lfsr1(8)]
            else:
                enc += [m | self.lfsr1(8), m & self.lfsr1(8)]
        return bytes(enc)