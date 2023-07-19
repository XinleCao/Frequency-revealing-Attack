import os.path
import random
import sys
import Density_attack
import Kerschbaum_encryption

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

yearly_plaintext = Load_data.load_Births(1, 12)  # load dataset

# attacking parameters
mu = 10
alpha = 15
gamma = 15
epsilon = 100
batch_count = 0

# security parameters
encrypt_tree = Kerschbaum_encryption.Tree()
min_value = 0
max_value = pow(2, 120)
tree_height = [0]

for i in sorted(yearly_plaintext)[len(yearly_plaintext) - 1:len(yearly_plaintext) - 1 - mu - 1:-1]:

    batch_count += 1

    # generate dataset in each batch
    current_dataset = []
    for j in yearly_plaintext[i]:
        current_dataset += [j[0]] * j[1]
    random.shuffle(current_dataset)

    # encryption
    for j in current_dataset:
        encrypt_tree.add(j, min_value, max_value)

    # traverse the encryption tree for sorted plaintexts and ciphertexts
    sorted_plaintexts = []
    sorted_ciphertexts = []
    encrypt_tree.in_order(encrypt_tree.root, sorted_plaintexts, sorted_ciphertexts, tree_height)

    # conducting density attack with alpha and gamma
    estimation = Density_attack.density_attack(sorted_ciphertexts, alpha, gamma)

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    frequency = Evaluation.calculate_frequency(sorted_plaintexts)
    accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

    print("With", batch_count, "batches of plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
          redundant_index)
    print("frequency: ", frequency)
    print("estimation: ", estimation, "\n")
