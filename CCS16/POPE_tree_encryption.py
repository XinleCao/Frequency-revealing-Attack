"""
This is the implementation of POPE.
Notably, we avoid the partial order-preserving property in POPE
as we focus on the property of frequency-hiding.
Moreover, the scenario of POPE fits our attacks well.
It assumes that there are lots of insertion operations and a few range queries.
The attacker may get a snapshot every time a few range queries are performed
and the orders a lot of inserted plaintexts are revealed.
"""

import random
from Crypto.Cipher import AES  # AES package
from Crypto.Util.Padding import pad
password = b'1234567887654321'


# a binary tree for encryption
class Node(object):
    """The basic structure in the POPE tree"""

    def __init__(self, plaintext=None, ciphertext=None):
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.lchild = None
        self.rchild = None


class Tree(object):
    """The POPE tree"""
    # data structure
    def __init__(self):
        self.root = None

    # add a new node (encryption algorithm)
    def add(self, x):
        """The encryption algorithm"""

        # define AES encryption
        global password
        aes = AES.new(password, AES.MODE_ECB)

        # adding the noise component
        if self.root is None:
            """The number of bits used to generate 
            noise is default as 64"""
            r = random.randint(0, pow(2, 64)) / pow(2, 64)
            y = x + r
            encode_y = pad(str.encode(str(y)), 16)
            en_y = aes.encrypt(encode_y)
            node = Node(y, en_y)
            self.root = node
            return node
        else:
            current_node = self.root

        # insert x into the POPE tree
        while 1:
            r = random.randint(0, pow(2, 64) - 1) / pow(2, 64)
            y = x + r

            if current_node.plaintext == y:
                continue
            elif current_node.plaintext > y:
                if current_node.lchild is None:
                    encode_y = pad(str.encode(str(y)), 16)
                    en_y = aes.encrypt(encode_y)
                    node = Node(y, en_y)
                    current_node.lchild = node
                    return node
                else:
                    current_node = current_node.lchild
            else:
                if current_node.rchild is None:
                    encode_y = pad(str.encode(str(y)), 16)
                    en_y = aes.encrypt(encode_y)
                    node = Node(y, en_y)
                    current_node.rchild = node
                    return node
                else:
                    current_node = current_node.rchild

    # return sorted plaintexts and ciphertexts
    def in_order(self, node, plaintexts, ciphertexts):
        """return sorted plaintexts and ciphertexts"""
        if node is None:
            return None

        self.in_order(node.lchild, plaintexts, ciphertexts)
        plaintexts.append(node.plaintext)
        ciphertexts.append(node.ciphertext)
        self.in_order(node.rchild, plaintexts, ciphertexts)


def encrypt(dataset):
    """function for encrypting a dataset"""
    if len(dataset) == 0:
        return None

    enc_tree = Tree()

    for i in dataset:
        enc_tree.add(i)

    # traverse the encryption tree
    plaintexts = []
    ciphertexts = []
    enc_tree.in_order(enc_tree.root, plaintexts, ciphertexts)
    return enc_tree, plaintexts, ciphertexts


"""
# mini test example
A = [1, 2, 3, 4]
A_ciphertext = encrypt(A)[2]
print(A_ciphertext)
"""

