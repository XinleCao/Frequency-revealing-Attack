import math


def density_attack(C, alpha, gamma):
    """
    density attack
    input: sorted ciphertexts C, interval length alpha, threshold gamma
    output: estimated upper bound ciphertext indexes pi_prime
    """

    pi_prime = []
    state = 1  # 1:increase stage, 0:decrease stage
    distance = -1
    order = 0  # index found

    for i in range(math.ceil(alpha / 2), len(C) - math.ceil(alpha / 2)):
        d = C[i + math.ceil(alpha / 2)] - C[i - math.ceil(alpha / 2)]

        if state == 1:  # increase stage
            if d > distance:
                distance = d
            elif d * gamma < distance:
                state = -1
                distance = d
                order = i

        elif state == -1:   # decrease stage
            if d < distance:
                distance = d
                order = i
            elif distance * gamma < d:
                state = 1
                distance = d
                pi_prime.append(order)

    pi_prime.append(len(C) - 1)
    return pi_prime
