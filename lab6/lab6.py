from gost341012 import EllipticCurve, sign, verify, prv_unmarshal, public_key
from gost341112 import GOST341112
import os


CURVE_PARAMS_TEXT = [
    (
      57896044618658097711785492504343953926634992332820282019728792003956564821041, # p
      57896044618658097711785492504343953927082934583725450622380973592137631069619, # q
      7, # a
      43308876546767276905765904595650931995942111794451039583252968842033849580414, # b
      2, # x
      4018974056539037503335449422937059775635739389905545080690979365213431566280, # y
    ),
    (
      3623986102229003635907788753683874306021320925534678605086546150450856166624002482588482022271496854025090823603058735163734263822371964987228582907372403,
      3623986102229003635907788753683874306021320925534678605086546150450856166623969164898305032863068499961404079437936585455865192212970734808812618120619743,
      7,
      1518655069210828534508950034714043154928747527740206436194018823352809982443793732829756914785974674866041605397883677596626326413990136959047435811826396,
      1928356944067022849399309401243137598997786635459507974357075491307766592685835441065557681003184874819658004903212332884252335830250729527632383493573274,
      2288728693371972859970012155529478416353562327329506180314497425931102860301572814141997072271708807066593850650334152381857347798885864807605098724013854
    )
]


def generate_keys(curve):
    privkey = prv_unmarshal(os.urandom(128))
    pubkey = public_key(curve, privkey)

    return pubkey, privkey


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        message = f.read()

    hashed_message = GOST341112(data=bytes(message, "utf-8")).digest()

    E = EllipticCurve(*(CURVE_PARAMS_TEXT[0]))
    public_key, private_key = generate_keys(E)

    signature = sign(E, private_key, hashed_message)

    with open("output.txt", "w") as f:
        f.write("Public key: " + str(public_key) + "\n")
        f.write("Private key: " + str(private_key) + "\n")
        f.write("Signature: " + str(signature) + "\n")
        f.write("Verification: " + str(verify(E, public_key, hashed_message, signature)))