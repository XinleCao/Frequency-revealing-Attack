import copy
import random

import Li_encryption
import Binomial_test_attack
# root dictionary
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

# load dataset
start_month = 1
end_month = 12
yearly_plaintext = Load_data.load_Births(start_month, end_month)

# encryption for the setup batch
current_dataset = []
for i in sorted(yearly_plaintext)[-1:-2:-1]:
    for j in yearly_plaintext[i]:
        current_dataset += [j[0]]*j[1]

random.shuffle(current_dataset)
ciphertexts = Li_encryption.encryption(current_dataset)
Li_encryption.flush(ciphertexts, 0)

# preserve the original frequency for evaluating accuracy and FP
original_frequency = Evaluation.calculate_frequency(ciphertexts)
print("original frequency:", original_frequency)
original_estimation_index_1 = []

mu = 10
alpha = 6500
gamma = 0.0000000000001
delta = 3000
epsilon = 100
for i in sorted(yearly_plaintext)[-2:-2-mu:-1]:

    # attack with insertion dataset
    current_dataset = []
    for j in range(len(yearly_plaintext[i])):
        item = yearly_plaintext[i][j]
        current_dataset += [item[0]] * item[1]

    random.shuffle(current_dataset)
    updated_ciphertexts, insertion_count = Li_encryption.insertion(ciphertexts,
                                                                   current_dataset)

    # apply the binomial test attack
    estimation_interval = Binomial_test_attack.find_interval(insertion_count,
                                                             alpha, gamma)
    estimation_index = Binomial_test_attack.find_prime(insertion_count,
                                                       estimation_interval, alpha, gamma, delta)

    # apply the attack on the setup batch
    original_estimation_index_2 = Binomial_test_attack.find_original_estimation_index(estimation_index,
                                                                                      ciphertexts, insertion_count, alpha, delta)
    original_estimation_index_1 = Binomial_test_attack.merge_estimation_index(original_estimation_index_1,
                                                                              original_estimation_index_2, delta)

    test_estimation_index = copy.deepcopy(original_estimation_index_1)
    test_estimation_index.append(original_frequency[-1])

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    accuracy, FP, redundant_index = Evaluation.evaluate(test_estimation_index, original_frequency, epsilon)
    print("With 2001 -", i, "batches of plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ", redundant_index)
    print("current estimation:", original_estimation_index_2)
    print("final estimation", test_estimation_index)
    print("original frequency", original_frequency)

    # flush for next round attack
    ciphertexts = copy.deepcopy(updated_ciphertexts)
    Li_encryption.flush(ciphertexts, 1)

    # evaluate the accuracy and false positive rata on the overall dataset under the absolute error epsilon
    print("Overall:")
    final_estimation = Binomial_test_attack.find_estimation(test_estimation_index, ciphertexts)
    print("final estimation:", final_estimation)


