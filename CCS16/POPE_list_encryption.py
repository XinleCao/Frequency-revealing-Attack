"""
To accelerate the encryption, we use bisect package
to assume the POPE tree is always balanced
Besides, we omit the AES encryption. To promise the same security,
we only allow the function return orders and insertion orders
to the attack function.
"""
import random
import bisect
from tqdm import tqdm
precision_bit = 32  # the number of bits for generating noise


def insert(plaintexts, x):
    """
    insert a plaintext in POPE
    plaintexts-prior encrypted plaintexts, x-a new plaintext
    return the insertion position (order) of x
    plaintexts are updated without being outputted
    """

    global precision_bit
    if len(plaintexts) == 0:
        r = random.randint(0, pow(2, precision_bit) - 1) / pow(2, precision_bit)
        y = x + r
        plaintexts.append(y)
        return 0

    # sample the random component and promise there is no repetition
    while 1:
        r = random.randint(0, pow(2, precision_bit) - 1) / pow(2, precision_bit)
        y = x + r
        insert_position = bisect.bisect_left(plaintexts, y)

        if insert_position == len(plaintexts):
            plaintexts.append(y)
            return insert_position
        elif y != plaintexts[insert_position]:
            plaintexts.insert(insert_position, y)
            return insert_position


def find_insert_position(plaintexts, x):
    """
    find the insertion position of x in plaintexts
    plaintexts-prior encrypted plaintexts, x-a new plaintext
    return the insertion position (order) of x
    plaintexts are not updated
    """
    global precision_bit
    if len(plaintexts) == 0:
        return 0

    while 1:
        r = random.randint(0, pow(2, precision_bit) - 1) / pow(2, precision_bit)
        y = x + r
        insert_position = bisect.bisect_left(plaintexts, y)

        if insert_position == len(plaintexts):
            return insert_position
        elif y != plaintexts[insert_position]:
            return insert_position


# insert a set insert_plaintexts to the old plaintexts
# input: old plaintexts, new plaintexts to be inserted
# output: a number list to indicate how many new plaintexts are inserted in each position
def insert_set(plaintexts, insert_plaintexts):
    """
    insert plaintexts in insert_plaintexts into plaintexts.
    plaintexts-prior encrypted plaintexts
    insert_plaintexts-plaintexts to be inserted
    return a number list to indicate how many new plaintexts
    are inserted in each position.
    """

    insertion_count = [0]*(len(plaintexts)+1)
    for i in tqdm(range(len(insert_plaintexts))):
        insert_position = find_insert_position(plaintexts, insert_plaintexts[i])
        insertion_count[insert_position] += 1
    return insertion_count

"""
# mini example
A = [1, 2, 3, 4]
plaintexts = []
for i in A:
    insert(plaintexts, i)
print(plaintexts)
"""

