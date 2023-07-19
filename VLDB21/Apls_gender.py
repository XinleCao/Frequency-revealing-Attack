import copy
import random

import Li_encryption
import Binomial_test_attack
# root dictionary
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

age, gender = Load_data.load_Apls()

# encryption for th setup batch
current_dataset = []
final_frequency = []
tmp = -1
for i in range(len(gender[0])):
    current_dataset += [i]*(gender[0][i])
    tmp += gender[0][i]
    final_frequency.append(tmp)
random.shuffle(current_dataset)

ciphertexts = Li_encryption.encryption(current_dataset)
Li_encryption.flush(ciphertexts, 0)

# preserve the original frequency for evaluating accuracy and FP
original_frequency = Evaluation.calculate_frequency(ciphertexts)
original_estimation_index_1 = []
print("frequency:", original_frequency)

alpha = 50000
mu = 4
gamma = 0.000001
delta = 30000
epsilon = 100


for i in range(1, len(gender)):

    print("The", i, "th insertion batch begins.", flush=True)
    print(len(ciphertexts))

    # attack with insertion batch
    current_dataset = []
    tmp = 0
    for j in range(len(gender[i])):
        current_dataset += [j]*(gender[i][j])
        tmp += gender[i][j]
        final_frequency[j] += tmp
    random.shuffle(current_dataset)
    updated_ciphertexts, insertion_count = Li_encryption.insertion(ciphertexts, current_dataset)

    if i <= mu:
        # apply the binomial test attack
        estimation_interval = Binomial_test_attack.find_interval(insertion_count, alpha*i, gamma)
        estimation_index = Binomial_test_attack.find_prime(insertion_count, estimation_interval, alpha*i, gamma, delta)

        # apply the attack on the setup batch
        original_estimation_index_2 = Binomial_test_attack.find_original_estimation_index(estimation_index,
                                                                                          ciphertexts, insertion_count,
                                                                                          alpha*i, delta)
        original_estimation_index_1 = Binomial_test_attack.merge_estimation_index(original_estimation_index_1,
                                                                                  original_estimation_index_2, delta)

        test_estimation_index = copy.deepcopy(original_estimation_index_1)
        test_estimation_index.append(original_frequency[-1])

        # evaluate the accuracy and false positive rata under the absolute error epsilon
        accuracy, FP, redundant_index = Evaluation.evaluate(test_estimation_index, original_frequency, epsilon)
        print("accuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
              redundant_index)
        print("current estimation:", original_estimation_index_2+[original_frequency[-1]])
        print("final estimation", original_estimation_index_1+[original_frequency[-1]])
        print("original frequency", original_frequency)

    # flush for next round attack
    ciphertexts = copy.deepcopy(updated_ciphertexts)
    Li_encryption.flush(ciphertexts, 1)

print("Overall dataset:")
final_estimation = Binomial_test_attack.find_estimation(test_estimation_index, ciphertexts)
print("final estimation", final_estimation)
print("original frequency", final_frequency)



