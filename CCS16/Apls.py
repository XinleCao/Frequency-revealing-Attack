import random
import POPE_list_encryption
import Fisher_test_attack
import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rebuilding_code.Common_functions import Evaluation, Load_data

age, gender = Load_data.load_Apls()

# attacking parameters
mu_age = 9
mu_gender = 4  # the number of gender insertion batch can be set from 2 to 35 (but we require it is smaller than 10 to guarantee a weaker attacker
alpha = 15000
gamma = 0.0001
epsilon = 100
age_insertion_count = []
gender_insertion_count = []

# age setup batch
plaintexts = []
current_dataset = []
final_frequency = []
tmp = -1
for i in range(len(age[0])):
    current_dataset += [i]*(age[0][i])
    tmp += age[0][i]
    final_frequency.append(tmp)
random.shuffle(current_dataset)
for i in current_dataset:
    POPE_list_encryption.insert(plaintexts, i)

for i in range(1, mu_age+1):
    print("the", i, "th age insertion batch begins.", flush=True)

    current_dataset = []
    tmp = 0
    for j in range(len(age[i])):
        current_dataset += [j]*(age[i][j])
        tmp += age[i][j]
        final_frequency[j] += tmp
    random.shuffle(current_dataset)

    age_current_insertion_count = POPE_list_encryption.insert_set(plaintexts, current_dataset)
    age_insertion_count.append(age_current_insertion_count)


# conducting Fisher exact test attack with alpha and gamma
estimation_interval = Fisher_test_attack.Fisher_exact_test_attack(mu_age, age_insertion_count, alpha, gamma)
estimation = Fisher_test_attack.find_index(mu_age, age_insertion_count, alpha, gamma, estimation_interval)
# add the last frequency index
estimation.append(len(plaintexts) - 1)

# evaluate the accuracy and false positive rata under the absolute error epsilon
frequency = Evaluation.calculate_frequency(plaintexts)
accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

print("Setup batch:")
print("With", mu_age, "batches of age insertion plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
        redundant_index, flush=True)
print("frequency: ", frequency, flush=True)
print("estimation: ", estimation, flush=True)

print("Overall dataset:")
final_estimation = Fisher_test_attack.calculate_final_index(mu_age, age_insertion_count, estimation)
print("frequency: ", final_frequency, flush=True)
print("estimation: ", final_estimation, flush=True)

# gender setup batch
plaintexts = []
current_dataset = []
final_frequency = []
tmp = -1
for i in range(len(gender[0])):
    current_dataset += [i]*(gender[0][i])
    tmp += gender[0][i]
    final_frequency.append(tmp)
random.shuffle(current_dataset)
for i in current_dataset:
    POPE_list_encryption.insert(plaintexts, i)

for i in range(1, len(gender)):
    print("the", i, "th gender insertion batch begins.", flush=True)

    current_dataset = []
    tmp = 0
    for j in range(len(gender[i])):
        current_dataset += [j]*(gender[i][j])
        tmp += gender[i][j]
        final_frequency[j] += tmp
    random.shuffle(current_dataset)

    gender_current_insertion_count = POPE_list_encryption.insert_set(plaintexts, current_dataset)
    gender_insertion_count.append(gender_current_insertion_count)


alpha = 15000
gamma = 0.00001

# conducting Fisher exact test attack with alpha and gamma
estimation_interval = Fisher_test_attack.Fisher_exact_test_attack(mu_gender, gender_insertion_count, alpha, gamma)
estimation = Fisher_test_attack.find_index(mu_gender, gender_insertion_count, alpha, gamma, estimation_interval)
# add the last frequency index
estimation.append(len(plaintexts) - 1)

# evaluate the accuracy and false positive rata under the absolute error epsilon
frequency = Evaluation.calculate_frequency(plaintexts)
accuracy, FP, redundant_index = Evaluation.evaluate(estimation, frequency, epsilon)

print("Setup batch:")
print("With", mu_gender, "batches of gender insertion plaintexts.", "\naccuracy: ", accuracy, "\nFP: ", FP, "\nredundant_index: ",
        redundant_index, flush=True)
print("frequency: ", frequency, flush=True)
print("estimation: ", estimation, flush=True)

print("Overall dataset:")
final_estimation = Fisher_test_attack.calculate_final_index(len(gender)-1, gender_insertion_count, estimation)
print("frequency: ", final_frequency, flush=True)
print("estimation: ", final_estimation, flush=True)