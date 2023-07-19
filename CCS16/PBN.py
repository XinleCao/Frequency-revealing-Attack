import copy
import random
import POPE_list_encryption
import Fisher_test_attack
import os.path
import sys
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

PBN = Load_data.load_PBN()[0]

for i in PBN:
    print(len(i))

# attacking parameters
mu = 4
alpha = 3000
gamma = 0.000000001
epsilon = 100
insertion_count = []

# setup batch
plaintexts = []
current_dataset = PBN[0]
for i in range(len(current_dataset)):
    POPE_list_encryption.insert(plaintexts, current_dataset[i])

frequency = Evaluation.calculate_frequency(plaintexts)

# insertion batches
for i in range(mu):
    print("the", i, "th insertion batch begins.", flush=True)
    current_dataset = PBN[i+1]
    current_insertion_count = POPE_list_encryption.insert_set(plaintexts, current_dataset)
    insertion_count.append(current_insertion_count)

# conducting Fisher exact test attack with alpha and gamma
estimation_interval = Fisher_test_attack.Fisher_exact_test_attack(mu, insertion_count, alpha, gamma)
estimation = Fisher_test_attack.find_index(mu, insertion_count, alpha, gamma, estimation_interval)
# add the last frequency index
estimation.append(len(plaintexts) - 1)

# evaluate the accuracy and false positive rata under the absolute error epsilon
frequency = Evaluation.calculate_frequency(plaintexts)
accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

print("With", i, "batches insertion plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP,
        "\nredundant_index: ", redundant_index, flush=True)
print("frequency: ", frequency, flush=True)
print("estimation: ", estimation, flush=True)

# evaluate the accuracy and false positive rata on the overall dataset under the absolute error epsilon
print("Overall:")
final_estimation = Fisher_test_attack.calculate_final_index(mu, insertion_count, estimation)
print("final estimation:", final_estimation)

