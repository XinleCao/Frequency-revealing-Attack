import random
import Kerschbaum_encryption
import Density_attack
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

PBN = Load_data.load_PBN()[0]

# attacking parameters
mu = 4
alpha = 15
gamma = 15
epsilon = 100

# security parameters
encryption_tree = Kerschbaum_encryption.Tree()
min_value = 0
max_value = pow(2, 120)

tree_height = [0]

for i in range(len(PBN)):

    # encryption
    current_dataset = PBN[i]
    for j in current_dataset:
        encryption_tree.add(j, min_value, max_value)

    # get ciphertexts
    sorted_plaintexts = []
    sorted_ciphertexts = []
    encryption_tree.in_order(encryption_tree.root, sorted_plaintexts, sorted_ciphertexts, tree_height)

    # conduct density attack
    estimation = Density_attack.density_attack(sorted_ciphertexts, alpha, gamma)

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    frequency = Evaluation.calculate_frequency(sorted_plaintexts)
    accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

    print("With", i + 1, "batches of plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
          redundant_index)
    print("frequency: ", frequency)
    print("estimation: ", estimation, "\n")

print("database size:", len(sorted_plaintexts))
print("tree height:", tree_height)
print("frequency:", frequency)
