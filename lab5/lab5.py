import math
import random
import os

enc = "iso-8859-1"

r =  [7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
      5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
      4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
      6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]

k = []
for i in range(0, 64):
    k.append(int(abs(math.sin(i+1)) * 2**32))

var = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
ipad_content = 0x36
opad_content = 0x5c

def rotate(x, y):
    x &= 0xFFFFFFFF

    return ((x<<y) | (x>>(32-y))) & 0xFFFFFFFF

def md5(message):
    block_size = 64

    message = bytearray(message)
    original_length_bit_message = (8 * len(message)) & 0xffffffffffffffff

    message.append(0x80)

    while len(message) % block_size != 56:
        message.append(0)

    message += original_length_bit_message.to_bytes(8, byteorder='little')

    messageA = var[0]
    messageB = var[1]
    messageC = var[2]
    messageD = var[3]

    for i in range(0, len(message), block_size):
        a = messageA
        b = messageB
        c = messageC
        d = messageD

        w = message[i : i + block_size]
        for j in range(block_size):
            if (0 <= j | j < 16):
                f = ((b & c) | (~b & d))
                g = j
            elif (j >= 16 | j < 32):
                f = ((d & b) | (~d & c))
                g = (5 * j + 1) % 16
            elif (j >= 32 | j < 48):
                f = (b ^ c ^ d)
                g = (3 * j + 5) % 16
            elif (j >= 48 | j < 64):
                f = (c ^ (b | (~d)))
                g = (7 * j) % 16

            tmp = (b+rotate(a+f+k[j]+int.from_bytes(w[4*g:4*g+4],
            byteorder='little'),r[j])) & 0xFFFFFFFF

            a, b, c, d = d, tmp, b, c

        messageA += a
        messageA &= 0xFFFFFFFF
        messageB += b
        messageB &= 0xFFFFFFFF
        messageC += c
        messageC &= 0xFFFFFFFF
        messageD += d
        messageD &= 0xFFFFFFFF

    x = messageA + (messageB << 32) + (messageC << 64) + (messageD << 96)

    return x.to_bytes(16, byteorder='little')


def to_hex(digest):
    return '{:032x}'.format(int.from_bytes(digest, byteorder='big'))


def getSalt():
    size = random.randint(1, 10)
    salt = ""

    for _ in range(0, size):
        salt += chr(random.randint(97, 122))

    return salt
def hmac(key, message, hash_function):
    block_size = 64

    opad = bytearray()
    ipad = bytearray()

    if len(key) > block_size:
        key = bytearray(hash_function(key))
    cpt = len(key)

    while block_size > cpt:
        cpt += 1
        key += b"\x00"

    for i in range(block_size):
        ipad.append(ipad_content ^ key[i])
        opad.append(opad_content ^ key[i])

    return hash_function(bytes(opad) + hash_function(bytes(ipad) + message))


def hmac_to_hex(hmac):
    return hmac.hex()


def convert_hex_to_ascii(h):
    chars_in_reverse = []

    while h != 0x0:
        chars_in_reverse.append(chr(h & 0xFF))
        h = h >> 8

    chars_in_reverse.reverse()

    return ''.join(chars_in_reverse)


if __name__ == '__main__':
    passwords = []

    for i in range(0, 100):
        id = "id" + str(i)
        size = random.randint(7, 14)
        value = ""

        for j in range(0, size):
            value += chr(random.randint(33, 122))

        salt = getSalt()

        passwords.append([id, to_hex(md5(bytes(value, enc))), [to_hex(md5(bytes(value + salt, enc))), salt],
        hmac_to_hex(hmac(bytes(salt, enc), bytes(value, enc), md5))])

    key = bytes(convert_hex_to_ascii(0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b), enc)


    with open('input.txt', "r") as f:
        message = f.read().encode("utf-8")

    with open('output.txt', "w") as f:
        f.write("hmac : " + str(hmac_to_hex(hmac(key, message, md5))))
