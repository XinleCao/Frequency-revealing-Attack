import copy


# input: a sorted number list
# output: a number list of cumulative frequency
# example: [0,0,0,1,1] -> [2,4]
def calculate_frequency(S):
    frequency = []
    for i in range(1, len(S)-1):

        # Kerschbaum's FH-OPE and POPE
        if type(S[i]) is not list:
            if int(S[i]) != int(S[i-1]):
                frequency.append(i-1)

        # FH-OPE proposed by Li et al.
        else:
            if S[i][0] != S[i-1][0]:
                frequency.append(i-1)

    # final plaintext frequency
    frequency.append(len(S)-1)
    return frequency


# function to calculate accuracy and false positive rate under absolute error epsilon
# input: estimation outputted by attacks, real frequencies, absolute error epsilon
# output: accuracy, false positive rate, FP estimations
def evaluate(estimation, frequency, epsilon):
    if estimation is None or len(estimation) == 0:
        return 0, 0, None

    # copy the output_results to complete removal
    estimation_copy = copy.deepcopy(estimation)

    for i in frequency:
        current_error = pow(2, 20)
        current_index = -1
        for j in estimation_copy:
            if abs(i - j) < current_error:
                current_index = j
                current_error = abs(i - j)
        if current_error < epsilon:
            estimation_copy.remove(current_index)

    # accuracy
    accuracy = (len(estimation) - len(estimation_copy)) / len(frequency)

    # false positive rate (FP)
    FP = len(estimation_copy) / len(frequency)

    # estimation_copy is returned to find which indexes are found wrong
    return accuracy, FP, estimation_copy


def evaluate_overall(frequency, estimation):
    "evaluate the recovery rate when combing sorting attack to recover plaintexts on the overall dataset"

    if estimation is None or len(estimation) == 0 or len(estimation) != len(frequency):
        print("wrong estimation!")
        exit(0)
    else:
        tmp = 0
        for i in range(len(estimation)):
            tmp += abs(estimation[i]-frequency[i])
        return 1 - tmp/frequency[-1]
