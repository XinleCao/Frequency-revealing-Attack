import copy
import random
import Li_encryption
import Binomial_test_attack
# root dictionary
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

PBN = Load_data.load_PBN()[0]

# encryption for the setup batch
ciphertexts = Li_encryption.encryption(PBN[0])
Li_encryption.flush(ciphertexts, 0)

# preserve the original frequency for evaluating accuracy and FP
original_frequency = Evaluation.calculate_frequency(ciphertexts)
original_estimation_index_1 = []

# attacking parameters
mu = 4
alpha = 25000
gamma = 0.0000000001
delta = 10000
epsilon = 100
del PBN[0]

for i in range(mu):

    # attack with insertion dataset
    updated_ciphertexts, insertion_count = Li_encryption.insertion(ciphertexts, PBN[0])
    del PBN[0]

    # apply the binomial test attack
    estimation_interval = Binomial_test_attack.find_interval(insertion_count, alpha*(i+1), gamma)
    estimation_index = Binomial_test_attack.find_prime(insertion_count, estimation_interval, alpha*(i+1), gamma, delta)

    # apply the attack on the setup batch
    original_estimation_index_2 = Binomial_test_attack.find_original_estimation_index(estimation_index, ciphertexts
                                                                                      ,insertion_count, alpha*(i+1), delta)
    original_estimation_index_1 = Binomial_test_attack.merge_estimation_index(original_estimation_index_1,
                                                                              original_estimation_index_2, delta)

    test_estimation_index = copy.deepcopy(original_estimation_index_1)
    test_estimation_index.append(original_frequency[-1])

    # evaluate the accuracy and false positive rata under the absolute error epsilon
    accuracy, FP, redundant_index = Evaluation.evaluate(test_estimation_index, original_frequency, epsilon)
    print("With ", i, " batches of plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
          redundant_index)
    print("current estimation:", original_estimation_index_2)
    print("final estimation", original_estimation_index_1)
    print("original frequency", original_frequency, flush = True)

    # flush for next round attack
    ciphertexts = copy.deepcopy(updated_ciphertexts)
    Li_encryption.flush(ciphertexts, 1)

    # evaluate the accuracy and false positive rata on the overall dataset under the absolute error epsilon
    print("Overall:")
    final_estimation = Binomial_test_attack.find_estimation(test_estimation_index, ciphertexts)
    print("final estimation:", final_estimation)
