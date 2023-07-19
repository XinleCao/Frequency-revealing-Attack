# root dictionary
import os.path
import sys
import random
import Fisher_test_attack
import POPE_list_encryption
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

yearly_plaintext = Load_data.load_Births(10, 12)

# setup batch
plaintexts = []
for i in sorted(yearly_plaintext)[-1:-2:-1]:
    current_dataset = []
    for j in range(len(yearly_plaintext[i])):
        item = yearly_plaintext[i][j]
        current_dataset += [item[0]]*item[1]
for i in current_dataset:
    POPE_list_encryption.insert(plaintexts, i)

# mu insertion batches
mu = 10
alpha = 500
gamma = 0.0000001
epsilon = 100
insertion_count = []

for i in sorted(yearly_plaintext)[-2:-2-mu:-1]:
    print("the ", i, " round begins.")
    current_dataset = []

    tmp = 0
    for j in range(len(yearly_plaintext[i])):
        item = yearly_plaintext[i][j]
        current_dataset += [item[0]]*item[1]

    random.shuffle(current_dataset)
    current_insertion_count = POPE_list_encryption.insert_set(plaintexts, current_dataset)
    insertion_count.append(current_insertion_count)

for i in range(2, mu+1):
    # conducting Fisher exact test attack with alpha and gamma
    estimation_interval = Fisher_test_attack.Fisher_exact_test_attack(i, insertion_count, alpha, gamma)
    estimation = Fisher_test_attack.find_index(i, insertion_count, alpha, gamma, estimation_interval)
    # add the last frequency index
    estimation.append(len(plaintexts)-1)

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    frequency = Evaluation.calculate_frequency(plaintexts)
    accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

    print("With", i, "batches of insertion plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ", redundant_index)
    print("frequency: ", frequency)
    print("estimation: ", estimation)


print("Overall dataset:")
final_estimation = Fisher_test_attack.calculate_final_index(mu, insertion_count, estimation)
print("estimation: ", final_estimation)