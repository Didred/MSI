from os import urandom


SIZE = 64


class EllipticCurve:
    def __iter__(self):
        for i in [self.p, self.q, self.a, self.b, self.x, self.y]:
            yield i

    def __init__(self, p, q, a, b, x, y):
        self.p = p
        self.q = q
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        r1 = self.y * self.y % self.p
        r2 = ((self.x * self.x + self.a) * self.x + self.b) % self.p

        if r2 < 0:
            r2 += self.p
        if r1 != r2:
            raise ValueError("Invalid parameters")

    def _pos(self, v):
        if v < 0:
            return v + self.p

        return v

    def _add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * modular_invert(2 * p1y, self.p)) % self.p
        else:
            tx = self._pos(p2x - p1x) % self.p
            ty = self._pos(p2y - p1y) % self.p
            t = (ty * modular_invert(tx, self.p)) % self.p

        tx = self._pos(t * t - p1x - p2x) % self.p
        ty = self._pos(t * (p1x - tx) - p1y) % self.p

        return tx, ty

    def exp(self, degree, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        degree -= 1

        if degree == 0:
            raise ValueError("Bad degree value")

        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)

            degree = degree >> 1
            x, y = self._add(x, y, x, y)

        return tx, ty


def public_key(curve, prv):
    return curve.exp(prv)


def sign(E_curve, private_key, message):
    size = 64
    q = E_curve.q
    e = to_int(message) % q

    if e == 0:
        e = 1

    while True:
        k = to_int(urandom(size)) % q

        if k == 0:
            continue

        r, _ = E_curve.exp(k)
        r %= q

        if r == 0:
            continue

        d = private_key * r
        k *= e
        s = (d + k) % q

        if s == 0:
            continue

        break

    return r, s


def verify(curve, public_key, message, signature):
    r, s = signature

    if len(to_bytes(s, SIZE) + to_bytes(r, SIZE)) != SIZE * 2:
        raise ValueError("Invalid signature length")

    q = curve.q
    p = curve.p

    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False

    e = to_int(message) % curve.q

    if e == 0:
        e = 1

    v = modular_invert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q

    p1x, p1y = curve.exp(z1)
    q1x, q1y = curve.exp(z2, public_key[0], public_key[1])
    lm = q1x - p1x

    if lm < 0:
        lm += p

    lm = modular_invert(lm, p)
    z1 = q1y - p1y

    lm = lm * z1 % p
    lm = lm * lm % p
    lm = lm - p1x - q1x
    lm = lm % p

    if lm < 0:
        lm += p

    lm %= q

    return lm == r


def prv_unmarshal(prv):
    return to_int(prv[::-1])


def pub_marshal(pub):
    return (to_bytes(pub[1], SIZE) + to_bytes(pub[0], SIZE))[::-1]


def pub_unmarshal(pub, mode=2012):
    pub = pub[::-1]

    return to_int(pub[SIZE:]), to_int(pub[:SIZE])


def to_int(raw):
    return int.from_bytes(raw, byteorder="big", signed=False)


def to_bytes(n, size=32):
    return int.to_bytes(n, byteorder="big", length=size, signed=False)


def modular_invert(a, n):
    if a < 0:
        return n - modular_invert(-a, n)

    t, newt = 0, 1
    r, newr = n, a

    while newr != 0:
        quotinent = r // newr
        t, newt = newt, t - quotinent * newt
        r, newr = newr, r - quotinent * newr

    if r > 1:
        return -1

    if t < 0:
        t = t + n

    return t
