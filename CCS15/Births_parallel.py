"""The implementation of the parallelism strategy"""
import math
import os.path
import random
import sys
import Density_attack
import Kerschbaum_encryption
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data, Threads

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
thread_num = 4

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
    threads = []
    n = len(sorted_ciphertexts)
    single_n = n//thread_num
    thread_range = [0]
    for item in range(thread_num):
        if item == thread_num-1:
            thread_range.append(n)
        else:
            thread_range.append(single_n*(item+1))
        thread = Threads.MyThread(Density_attack.density_attack, args = [sorted_ciphertexts[thread_range[item]:thread_range[item+1]], alpha, gamma,])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    estimations = []
    count = 0
    for thread in threads:
        tmp = thread.get_result()
        if count < thread_num - 1:
            del tmp[-1]
        for h in range(len(tmp)):
            tmp[h] += thread_range[count]
        estimations.append(tmp)
        count += 1

    estimation = []
    print(estimations)
    for item in range(thread_num-1):
        estimation += estimations[item]
        if len(estimations[item]) > 0 or len(estimations[item+1]) > 0:
            last_index = estimations[item][-1] - math.ceil(alpha/2)
            next_index = estimations[item+1][0] + math.ceil(alpha/2)
            tmp = Density_attack.density_attack(sorted_ciphertexts[last_index:next_index+1], alpha, gamma)
            for h in range(len(tmp)):
                tmp[h] += last_index
            if len(tmp) > 0:
                del tmp[-1]
            estimation += tmp
    estimation += estimations[-1]

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    frequency = Evaluation.calculate_frequency(sorted_plaintexts)
    accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

    print("With", batch_count, "batches of plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
          redundant_index)
    print("frequency: ", frequency)
    print("estimation: ", estimation, "\n")
