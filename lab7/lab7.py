from ecdsa.keys import SigningKey


def md5(text):
    from md5 import MD5

    text_hash = MD5().md5(text.encode(), hex_result=True)
    return text_hash


def sha256(text):
    from hashlib import sha256

    text_hash = sha256(text.encode()).hexdigest()
    return text_hash


def sha512(text):
    from hashlib import sha512

    text_hash = sha512(text.encode()).hexdigest()
    return text_hash


def get_hash(text, hash_func=sha256):
    return hash_func(text)


if __name__ == "__main__":
    a = SigningKey.generate()
    a_private = a.privkey.secret_multiplier
    a_public = a.verifying_key.pubkey.point

    b = SigningKey.generate()
    b_private = b.privkey.secret_multiplier
    b_public = b.verifying_key.pubkey.point

    a_b_key = str(a_public * b_private)
    b_a_key = str(b_public * a_private)

    with open("output.txt", "w") as f:
        f.write(
f"""Секретный ключ #1 : {a_private}
Публичный ключ #1 : {a_public}
Секретный ключ #2 : {b_private}
Публичный ключ #2 : {b_public}
Секретный ключ #2 * Публичный ключ #1 : {a_b_key}
Публичный ключ #1 * Секретный ключ #2 : {b_a_key}
Hash(Секретный ключ #2 * Публичный ключ #1) : {get_hash(a_b_key)}
Hash(Публичный ключ #1 * Секретный ключ #2) : {get_hash(b_a_key)}
Ключи и хеши эквивалентны : {a_b_key == b_a_key and get_hash(a_b_key) == get_hash(b_a_key)}"""
)