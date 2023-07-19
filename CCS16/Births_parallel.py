# root dictionary
import copy
import math
import os.path
import sys
import random
import tqdm
import Fisher_test_attack
import POPE_list_encryption
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data, Threads

yearly_plaintext = Load_data.load_Births(1, 12)

# setup batch
plaintexts = []
for i in sorted(yearly_plaintext)[-1:-2:-1]:
    current_dataset = []
    for j in yearly_plaintext[i]:
        current_dataset += [j[0]]*j[1]
random.shuffle(current_dataset)
for i in tqdm.tqdm(range(len(current_dataset))):
    POPE_list_encryption.insert(plaintexts, current_dataset[i])

# mu insertion batches
mu = 10
alpha = 500
gamma = 0.0000001
epsilon = 100
insertion_count = []
thread_num = 4

for i in sorted(yearly_plaintext)[-2:-2-mu:-1]:
    print("the ", i, " round begins.")
    current_dataset = []
    for j in yearly_plaintext[i]:
        current_dataset += [j[0]]*j[1]

    random.shuffle(current_dataset)
    current_insertion_count = POPE_list_encryption.insert_set(plaintexts, current_dataset)
    insertion_count.append(current_insertion_count)

for i in range(mu, mu-1, -1):
    # conducting Fisher exact test attack with alpha and gamma
    threads = []
    n = len(plaintexts)
    single_n = n//thread_num
    thread_range = [0]

    for item in range(thread_num):
        if item == thread_num-1:
            thread_range.append(n)
        else:
            thread_range.append(single_n*(item+1))
        tmp_insertion_count = []
        for j in range(len(insertion_count)):
            tmp_insertion_count.append(copy.deepcopy(insertion_count[j][thread_range[item]:thread_range[item+1]+1]))
        thread = Threads.MyThread(Fisher_test_attack.direct_find_index, args=[i, tmp_insertion_count,
                                                            alpha, gamma,])
        thread.start()
        threads.append(thread)

    print(thread_range)
    frequency = Evaluation.calculate_frequency(plaintexts)
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

    for item in range(thread_num-1):
        estimation += estimations[item]
        if len(estimations[item])>0 and len(estimations[item+1])>0:
            last_index = estimations[item][-1] - alpha
            next_index = estimations[item+1][0] + alpha
            tmp_insertion_count = []
            for j in range(len(insertion_count)):
                tmp_insertion_count.append(copy.deepcopy(insertion_count[j][last_index:next_index+1]))
            tmp_interval = Fisher_test_attack.Fisher_exact_test_attack(i, tmp_insertion_count, alpha, gamma)
            print(tmp_interval)
            tmp_index = Fisher_test_attack.find_index(i, tmp_insertion_count, alpha, gamma, tmp_interval)
            print(tmp_index)
            if len(tmp_index)>=2:
                del tmp_index[-1]
                del tmp_index[0]
            for h in range(len(tmp_index)):
                tmp_index[h] += last_index
            estimation += tmp_index
    # add the last frequency index
    estimation += estimations[-1]
    estimation.append(len(plaintexts)-1)

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    frequency = Evaluation.calculate_frequency(plaintexts)
    accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

    print("With", i, "batches of insertion plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ", redundant_index)
    print("frequency: ", frequency)
    print("estimation: ", estimation, flush=True)

