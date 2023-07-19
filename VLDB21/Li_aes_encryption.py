"""
This is the code of the FH-OPE scheme proposed in VLDB 2021
"""

import random

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

password = b'1234567887654321'


# encryption with aes
# input: old ciphertexts, a new plaintext x, local table LT
# output: a new ciphertext y, ciphertexts are updated without being outputted
def encrypt_with_aes(ciphertexts, x, LT):
    """
    Encryption algorithm with aes
    :param ciphertexts: prior ciphertexts encrypted
    :param x: the new plaintext to be inserted
    :param LT: the local table stored in the client
    :return: updated ciphertexts where the ciphertext of x is inserted
    """

    # AES encryption
    global password
    y = AES.new(password, AES.MODE_ECB)

    # find insertion position according to LT
    left_position = None
    right_position = None
    for item in LT:
        if item < x:
            left_position += LT[item]
        if item <= x:
            right_position += LT[item]
    insert_position = random.randint(left_position, right_position)

    # insertion
    ciphertexts.insert(insert_position, y)

    # update the local table
    if x in LT:
        LT[x] += 1
    else:
        LT[x] = 1

    return ciphertexts
