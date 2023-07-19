import copy
import math
import random

import Li_encryption
import Binomial_test_attack
# root dictionary
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data, Threads

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
original_estimation_index_1 = []

alpha = 5000
gamma = 0.000000000000001
delta = 3000
epsilon = 100
thread_num = 4

count_year = 0

for i in sorted(yearly_plaintext)[(len(yearly_plaintext)-2):0:-1]:

    # attack with insertion dataset
    current_dataset = []
    for j in yearly_plaintext[i]:
        current_dataset += [j[0]] * j[1]

    random.shuffle(current_dataset)
    updated_ciphertexts, insertion_count = Li_encryption.insertion(ciphertexts,
                                                                   current_dataset)

    threads = []
    n = len(ciphertexts)
    single_n = n // thread_num
    thread_range = [0]

    for item in range(thread_num):
        if item == thread_num - 1:
            thread_range.append(n)
        else:
            thread_range.append(single_n * (item + 1))
        tmp_insertion_count = copy.deepcopy(insertion_count[thread_range[item]:thread_range[item + 1] + 1])
        thread = Threads.MyThread(Binomial_test_attack.directly_find_index, args=[tmp_insertion_count, alpha*(count_year+1), gamma, delta, ])
        thread.start()
        threads.append(thread)

    print(thread_range)
    frequency = Evaluation.calculate_frequency(ciphertexts)
    print(frequency)
    for thread in threads:
        thread.join()

    estimations = []
    count = 0
    for thread in threads:
        tmp = thread.get_result()
        for h in range(len(tmp)):
            tmp[h] += thread_range[count]
        estimations.append(tmp)
        count += 1

    estimation = []
    print(estimations)

    for item in range(thread_num - 1):
        estimation += estimations[item]
        if len(estimations[item]) > 0 and len(estimations[item + 1]) > 0:
            last_index = estimations[item][-1] - math.ceil(alpha/2)
            next_index = estimations[item + 1][0] + math.ceil(alpha/2)
            tmp_insertion_count = copy.deepcopy(insertion_count[last_index:next_index + 1])
            tmp_interval = Binomial_test_attack.find_interval(tmp_insertion_count, alpha*(count_year+1), gamma)
            print(tmp_interval)
            tmp_index = Binomial_test_attack.find_prime(tmp_insertion_count, tmp_interval, alpha*(count_year+1), gamma, delta)
            print(tmp_index)
            if len(tmp_index) >= 2:
                del tmp_index[-1]
                del tmp_index[0]
            for h in range(len(tmp_index)):
                tmp_index[h] += last_index
            estimation += tmp_index
    # add the last frequency index
    estimation += estimations[-1]
    estimation_index = estimation

    # apply the attack on the setup batch
    original_estimation_index_2 = Binomial_test_attack.find_original_estimation_index(estimation_index,
                                                                                      ciphertexts, insertion_count, alpha*(count_year+1), delta)
    original_estimation_index_1 = Binomial_test_attack.merge_estimation_index(original_estimation_index_1,
                                                                              original_estimation_index_2, delta)

    test_estimation_index = copy.deepcopy(original_estimation_index_1)
    test_estimation_index.append(original_frequency[-1])

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    accuracy, FP, redundant_index = Evaluation.evaluate(test_estimation_index, original_frequency, epsilon)
    print("With 2001 -", i, "batches of plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ", redundant_index)
    print("current estimation:", original_estimation_index_2)
    print("final estimation", original_estimation_index_1)
    print("original frequency", original_frequency, flush=True)

    # flush for next round attack
    ciphertexts = copy.deepcopy(updated_ciphertexts)
    Li_encryption.flush(ciphertexts, 1)
    count_year += 1


