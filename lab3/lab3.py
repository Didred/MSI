import random


MILLER_RABIN_CERTAINTY = 50
PRIME_MIN = 10 ** 100
PRIME_MAX = 10 ** 150


def are_coprime(a, b):
    while b:
        a, b = b, a % b

    if a == 1:
        return True

    return False


def mod_inverse(a, b):
    x = 0
    ox = 1
    ob = b

    while b:
        a, q, b = b, a // b, a % b
        x, ox = ox - (q * x), x

    return ox % ob


def miller_rabin(n):
    if n % 2 == 0 or n % 3 == 0:
        return False
        
    d = n - 1
    r = 0

    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(MILLER_RABIN_CERTAINTY):
        a = random.randrange(2, n - 1)
        v = pow(a, d, n)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == r - 1:
                    return False
                else:
                    i += 1
                    v = pow(v, 2, n)
    return True


def generate_keys():
    while 1:
        p = random.randint(PRIME_MIN, PRIME_MAX)
        if miller_rabin(p):
            break

    while 1:
        q = random.randint(PRIME_MIN, PRIME_MAX)
        if miller_rabin(q) and p != q:
            break

    n = p * q
    phi_n = (p - 1) * (q - 1)

    while 1:
        e = random.randint(2, phi_n - 1)
        if are_coprime(e, phi_n):
            break

    d = mod_inverse(e, phi_n)

    return e, d, n


def encrypt(string, e, n):
    msg_bin = "".join(bin(ord(c))[2:].zfill(8) for c in string)

    for i in range(256):
        new_msg_bin = msg_bin + bin(i)[2:].zfill(8)
        if are_coprime(int(new_msg_bin, 2), n):
            m = int(new_msg_bin, 2)
            break

    c = pow(m, e, n)

    return c


def decrypt(c, d, n):
    m = pow(c, d, n)
    binstr = bin(m)[2:]

    while len(binstr) % 8 != 0:
        binstr = "0" + binstr

    msg = ""
    binstr = binstr[:-8]

    for i in range(0, len(binstr), 8):
        msg += chr(int(binstr[i:i + 8], 2))

    return msg


def main():
    e, d, n = generate_keys()

    with open('input.txt') as f:
        text = f.read()

    msg = encrypt(text, e, n)
    with open('output_encrypted.txt', "w") as f:
        f.write(str(msg))

    with open("output_decrypted.txt", "w") as f:
        f.write(decrypt(msg, d, n))


if __name__ == '__main__':
    main()
