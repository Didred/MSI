from PIL import Image
from utils import *


def insert_into_pixel(r, g, b, val):
    if len(val) == 1:
        val += "00"
    elif len(val) == 2:
        val += "0"

    x, y, z = tuple(map(int, val))

    r = insert_into_byte(r, x)
    g = insert_into_byte(g, y)
    b = insert_into_byte(b, z)

    return (r, g, b)


def alignedbin32(val):
    binary = bin(val)[2:]

    if len(binary) < 32:
       binary = "0" * (32 - len(binary)) + binary

    return binary


def tobits(s):
    result = ''

    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result += bits

    return ''.join(result)


def frombits(bits):
    chars = []

    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

    return ''.join(chars)


def insert_into_byte(byte, bit):
    return ((byte >> 1) << 1) | bit

def encode(message):
    img = Image.open('input.png')
    pixels = img.load()

    message_bits = tobits(message)

    length = alignedbin32(len(message_bits))
    bits_count = length + message_bits

    pixel_count = 0

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixel_count >= len(bits_count):
                break

            r, g, b = pixels[i, j]

            temp = bits_count[pixel_count : pixel_count + 1 * 3]

            pixels[i, j] = insert_into_pixel(r, g, b, temp)

            pixel_count += 3

    new_img = Image.new(img.mode, img.size)
    new_pixels = new_img.load()

    for i in range(new_img.size[0]):
        for j in range(new_img.size[1]):
            new_pixels[i, j] = pixels[i, j]

    new_img.save('output.png')


def decode():
    img = Image.open('output.png')
    pixels = img.load()

    hidden_bits = ""
    length = 10 ** 8
    check = False

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if (not check and len(hidden_bits) > 32):
                    length = int(hidden_bits[:32], base=2)
                    hidden_bits = hidden_bits[32:]
                    check = True

            if len(hidden_bits) > length:
                break

            r, g, b = pixels[i, j]
            hidden_bits += str(r & 1) + str(g & 1) + str(b & 1)

    hidden_bits = hidden_bits[:length]
    hidden_message = frombits(hidden_bits)

    return hidden_message


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        message = f.read()

    encode(message)
    hidden_message = decode()

    with open("output.txt", "w") as f:
        f.write("message : " + message)
        f.write("\nhidden_message : " + hidden_message)

        if message == hidden_message:
            f.write("\nTrue")
        else:
            f.write("\nFalse")