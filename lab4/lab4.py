import random
import math
import primes


def exp(base, power, m):
    result = 1
    for _ in range(power):
        result = (result * base) % m
    return result


def get_p():
    a = primes.a

    rand = random.randint(100, len(a))

    return a[rand]


def get_fact(p):
    fact = []
    n = p - 1
    
    for i in range(2, int(math.sqrt(n))):
        if n % i == 0:
            fact.append(i)
            while n % i == 0:
                n /= i

    if n > 1:
        fact.append(n)
        
    return fact


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def get_antiderivative_root(p, fact):
    g = random.randint(2, p - 1)

    for i in range(len(fact)):
        if exp(g, int((p - 1) / fact[i]), p) == 1:
            return get_antiderivative_root(p, fact)

    return g


def get_k(p):
    while True:
        k = random.randint(1, p - 1)
        if gcd(k, p - 1) == 1:
            return k


def generate_keys():
    p = get_p()

    g = get_antiderivative_root(p, get_fact(p))

    x = random.randint(2, p - 1)
    y = exp(g, x, p)

    print() 

    print("  Открытые ключи:")
    print(f"     p = {p}")
    print(f"     g = {g}")
    print(f"     y = {y}")

    print()

    print("  Закрытый ключ")
    print(f"     x = {x}")

    print()

    return {"p": p, "g": g, "y": y}, x


def encrypt(message, p, g, y):
    encrypted = []

    for m in message:
        k = get_k(p)

        a = exp(g, k, p)
        b = exp(y, k, p)
        b = (b * m) % p

        encrypted.append(a)
        encrypted.append(b)

    return encrypted


def decrypt(message, p, x):
    decrypted = []
    
    for i in range(0, len(message) - 1, 2):
        a = message[i]
        b = message[i + 1]

        m = (b * a ** (p - 1 - x)) % p

        decrypted.append(chr(m))

    return decrypted


if __name__ == "__main__":
    public_keys, private_key = generate_keys()

    with open("input.txt", "r") as f:
        message = f.readline()
    
    message_chars = []
    for m in message:
        message_chars.append(ord(m))

    encrypted = encrypt(message_chars, public_keys["p"], public_keys["g"], public_keys["y"])
    with open('output_encrypted.txt', "w") as f:
        f.write(str(encrypted))

    decrypted = decrypt(encrypted, public_keys["p"], private_key)
    with open("output_decrypted.txt", "w") as f:
        f.write("".join(decrypted))
