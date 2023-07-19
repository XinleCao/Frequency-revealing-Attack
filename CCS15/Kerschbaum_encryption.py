"""
This is the implementation of Kerschaum's FH-OPE scheme
"""

import random
import math


class Node(object):
    """The basic node structure in the encryption tree of Kerschbaum's FH-OPE"""

    def __init__(self, plaintext=None, ciphertext=None, height=None):
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.lchild = None
        self.rchild = None
        self.height = height
        self.lchild_num = 0
        self.rchild_num = 0


class Tree(object):
    """The encryption tree of Kerschbaum's FH-OPE scheme"""

    def __init__(self):
        self.root = None

    def add(self, x, pre_value, post_value):
        """add a new node (encryption algorithm)"""
        if abs(post_value - pre_value) < 8:
            print("wrong: the ciphertext space is too small!")

        if self.root is None:
            node = Node(x, pre_value + math.ceil((post_value - pre_value) / 2), 0)
            self.root = node
            return node
        else:
            current_node = self.root

        while 1:
            if current_node.plaintext == x:
                random_coin = random.randint(0, 1)
            else:
                random_coin = None

            if current_node.plaintext > x or random_coin == 0:  # traverse left
                current_node.lchild_num += 1
                post_value = current_node.ciphertext
                if current_node.lchild is None:
                    node = Node(x, pre_value + math.ceil((post_value - pre_value) / 2), current_node.height+1)
                    current_node.lchild = node
                    return node
                else:
                    current_node = current_node.lchild
            else:
                pre_value = current_node.ciphertext  # traverse right
                current_node.rchild_num += 1
                if current_node.rchild is None:
                    node = Node(x, pre_value + math.ceil((post_value - pre_value) / 2), current_node.height+1)
                    current_node.rchild = node
                    return node
                else:
                    current_node = current_node.rchild

    def insert(self, x, pre_value, post_value):
        left = 0
        right = 0
        """add a new node (encryption algorithm)"""
        if abs(post_value - pre_value) < 8:
            print("wrong: the ciphertext space is too small!")

        if self.root is None:
            node = Node(x, pre_value + math.ceil((post_value - pre_value) / 2), 0)
            self.root = node
            return node
        else:
            current_node = self.root

        while 1:
            if current_node.plaintext == x:
                random_coin = random.randint(0, 1)
            else:
                random_coin = None

            if current_node.plaintext > x or random_coin == 0:  # traverse left
                right = right + 1 + current_node.rchild_num
                post_value = current_node.ciphertext
                if current_node.lchild is None:
                    return left, right
                else:
                    current_node = current_node.lchild
            else:
                pre_value = current_node.ciphertext  # traverse right
                left = left + 1 + current_node.lchild_num
                if current_node.rchild is None:
                    return left, right
                else:
                    current_node = current_node.rchild

    def in_order(self, node, sorted_plaintexts, sorted_ciphertexts, tree_height):
        """return sorted plaintexts and ciphertexts"""

        if node is None:
            return None

        self.in_order(node.lchild, sorted_plaintexts, sorted_ciphertexts, tree_height)
        sorted_plaintexts.append(node.plaintext)
        sorted_ciphertexts.append(node.ciphertext)
        if node.height > tree_height[0]:
            tree_height[0] = node.height
        self.in_order(node.rchild, sorted_plaintexts, sorted_ciphertexts, tree_height)


def encrypt(dataset, min_value, max_value):
    """function for encrypting a dataset"""
    if len(dataset) == 0:
        return None

    encrypt_tree = Tree()
    for i in dataset:
        encrypt_tree.add(i, min_value, max_value)

    # traverse the encryption tree
    sorted_plaintexts = []
    sorted_ciphertexts = []
    tree_height = [0]
    encrypt_tree.in_order(encrypt_tree.root, sorted_plaintexts, sorted_ciphertexts, tree_height)
    return encrypt_tree, sorted_plaintexts, sorted_ciphertexts, tree_height



# mini test example
# A = [1,4,2,6,7,5,9]
# A_ciphertext = encrypt(A, 0, 128)[2]
# print(A_ciphertext)
