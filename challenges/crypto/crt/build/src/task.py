from Crypto.Util.number import getPrime, bytes_to_long
import secrets

# Step 1. 生成两个足够长的安全素数
p = getPrime(256)
q = getPrime(256)

# Step 2. 计算两个素数的乘积，有欧拉函数 φ(n)=φ(p)φ(q)
n = p*q
phi = (p-1)*(q-1)

# Step 3. 选择公钥指数 e，满足 e 与欧拉函数 φ(n) 互质
e = 17
if phi % e == 0: # 重新选择 e
    ... # 省略
else: # Step 4. 计算私钥指数 d，满足 e*d ≡ 1 (mod φ(n))
    d = pow(e, -1, phi)
    assert (e*d) % phi == 1

flag = open('/flag', 'rb').read().strip()
assert len(flag) == 44

def pad(m):
    # return flag + secrets.token_bytes(62-len(flag)) + bytes([len(flag)])
    return flag + b"\x85"*(62-len(flag)) + bytes([len(flag)])

# Step 5. 将明文进行填充，并转换为整数 m
m = bytes_to_long(pad(flag))

# Step 6. 计算密文 c
c = pow(m, e, n)

print(f'{n = }')
print(f'{c = }')
