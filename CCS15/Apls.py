import random
import Kerschbaum_encryption
import Density_attack
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

age, gender = Load_data.load_Apls()

# attacking parameters
alpha = 15
gamma = 15
epsilon = 100

# security parameters
encryption_age_tree = Kerschbaum_encryption.Tree()
encryption_gender_tree = Kerschbaum_encryption.Tree()
min_value = 0
max_value = pow(2, 120)
tree_height = [0]
sorted_plaintexts = []
sorted_ciphertexts = []

for i in range(len(age)):

    """Age dataset"""
    current_age_dataset = []

    # generate dataset in each batch
    for j in range(len(age[i])):
        current_age_dataset += [j] * age[i][j]
    random.shuffle(current_age_dataset)

    # encryption
    for j in current_age_dataset:
        encryption_age_tree.add(j, min_value, max_value)

    # get ciphertexts
    sorted_plaintexts = []
    sorted_ciphertexts = []
    encryption_age_tree.in_order(encryption_age_tree.root, sorted_plaintexts, sorted_ciphertexts, tree_height)

# conduct density attack
estimation = Density_attack.density_attack(sorted_ciphertexts, alpha, gamma)

# evaluate the accuracy and false positive rata under the absolute error epsilon
frequency = Evaluation.calculate_frequency(sorted_plaintexts)
accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

print("With", i + 1, "batches of age plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
      redundant_index)
print("frequency: ", frequency)
print("estimation: ", estimation, "\n")

for i in range(len(gender)):

    """Gender dataset"""
    current_gender_dataset = []

    # generate dataset in each batch
    for j in range(len(gender[i])):
        current_gender_dataset += [j] * gender[i][j]
    random.shuffle(current_gender_dataset)

    # encryption
    for j in current_gender_dataset:
        encryption_gender_tree.add(j, min_value, max_value)

    # get ciphertexts
    sorted_plaintexts = []
    sorted_ciphertexts = []
    encryption_age_tree.in_order(encryption_gender_tree.root, sorted_plaintexts, sorted_ciphertexts, tree_height)

print("dataset size:", len(sorted_plaintexts))
print("tree height:", tree_height)
# conduct density attack
estimation = Density_attack.density_attack(sorted_ciphertexts, alpha, gamma)

# evaluate the accuracy and false positive rata under the absolute error epsilon
frequency = Evaluation.calculate_frequency(sorted_plaintexts)
accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

print("With", i + 1, "batches of gender plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
    redundant_index)
print("frequency: ", frequency)
print("estimation: ", estimation, "\n")

print("dataset size:", len(sorted_plaintexts))
print("tree height:", tree_height)
