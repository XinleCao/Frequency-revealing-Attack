"""
To accelerate the encryption, we use bisect package
to assume the coding tree is always a balanced binary tree.
Besides, we omit the AES encryption. To promise the same security,
we only allow the function return orders and insertion orders
to the attack function.
"""

import random
import copy
from tqdm import tqdm


def list_bisect_left(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the|
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid][0] < x[0]: lo = mid+1
        else: hi = mid
    return lo


def list_bisect_right(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x[0] < a[mid][0]: hi = mid
        else: lo = mid+1
    return lo


def encryption(plaintexts):
    """
    The encryption algorithm for encrypting a dataset.
    :param plaintexts: a dataset.
    :return: the ciphertexts of the dataset
    """
    ciphertexts = []

    # [item, -1, -1]: the second (third) index is used to mark the position in the last (setup) batch
    for i in tqdm(range(len(plaintexts))):
        item = plaintexts[i]
        left_index = list_bisect_left(ciphertexts, [item, -1, -1])
        right_index = list_bisect_right(ciphertexts, [item, -1, -1])
        insertion_index = random.randint(left_index, right_index)
        ciphertexts.insert(insertion_index, [item, -1, -1])

    return ciphertexts


# insert the insertion batches
# input: the ciphertexts, count_insertion (used to record the insertion process), insertion batch
# output: updated ciphertexts, the updated count_insertion
def insertion(ciphertexts, insertion_batch):
    """
    The insertion algorithm for inserting an insertion batch.
    :param ciphertexts: ciphertexts of the setup batch.
    :param insertion_batch.
    :return: ciphertexts updated with the insertion batch,
            the list recording the insertion process.
    """

    count_insertion = [0]*len(ciphertexts) + [0]
    updated_ciphertexts = copy.deepcopy(ciphertexts)
    for i in tqdm(range(len(insertion_batch))):
        item = insertion_batch[i]

        left_index = list_bisect_left(updated_ciphertexts, [item, -1, -1])
        right_index = list_bisect_right(updated_ciphertexts, [item, -1, -1])
        insertion_index = random.randint(left_index, right_index)
        updated_ciphertexts.insert(insertion_index, [item, -1, -1])

        # find the insertion position in ciphertexts (not updated_ciphertexts)
        left_flag = 0
        for j in range(insertion_index-1, -1, -1):
            if updated_ciphertexts[j][1] != -1:
                count_insertion[updated_ciphertexts[j][1]+1] += 1
                left_flag = 1
                break

        if left_flag == 0:
            count_insertion[0] += 1

    return updated_ciphertexts, count_insertion


def flush(ciphertexts, flag=0):
    """
    Flush ciphertexts for insertion of the new insertion batch.
    :param ciphertexts: prior ciphertexts.
    :param flag: 0-this is a setup batch; 1-this is a union of a setup batch and insertion batches.
    :return: ciphertexts prepared for insertion.
    """

    if flag == 0:
        for i in range(len(ciphertexts)):
            ciphertexts[i][1] = i
            ciphertexts[i][2] = i
    else:
        for i in range(len(ciphertexts)):
            ciphertexts[i][1] = i
