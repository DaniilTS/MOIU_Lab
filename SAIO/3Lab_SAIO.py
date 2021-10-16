import numpy as np


def resource_allocation_task(A):
    shape = A.shape
    n = shape[0]
    Q = shape[1] - 1

    x, opt = fill_first_row(A, n, Q)
    x, opt = fillNthRows(A, x, opt)

    x_arr = allocate_resources(x, n, Q)

    return x, opt, x_arr


def allocate_resources(x, n, Q):
    x_arr = []
    for i in reversed(range(n)):
        elem = x[i][Q]
        x_arr.append(elem)
        Q = int(Q - elem)

    return x_arr


def fillNthRows(A, x, opt):
    temp_x = np.copy(x)
    temp_opt = np.copy(opt)
    for n, row in enumerate(A[1:]):
        for q, el in enumerate(row):
            opt_pairs = generate_pairs(n, q, reverse=True)  # левая колонка
            A_pairs = generate_pairs(n + 1, q)  # правая колонка
            best_pair = find_best_pair(A, temp_opt, opt_pairs, A_pairs)
            temp_opt[n + 1][q] = best_pair[0]
            temp_x[n + 1][q] = best_pair[1]

    return temp_x, temp_opt


def find_best_pair(A, opt, opt_pairs, A_pairs):
    pairs_sum = []
    for i, (opt_indexes, A_indexes) in enumerate(zip(opt_pairs, A_pairs)):
        opt_value = opt[opt_indexes[0]][opt_indexes[1]]
        A_value = A[A_indexes[0]][A_indexes[1]]
        sum = opt_value + A_value
        pairs_sum.append([sum, A_indexes[1]])  # A_indexes[1] - сколько ресурсов отдали последнему агенту

    result = sorted(pairs_sum)  # key - сумма пары

    return result[-1]


def generate_pairs(first_num, q, reverse=False):
    pairs = []
    for num in range(0, q + 1):
        pairs.append([first_num, num])

    if reverse:
        pairs.reverse()

    return pairs


def fill_first_row(A, n, Q):
    x = opt = np.zeros((n, Q + 1))
    for i, row in enumerate(A[:1]):
        for j, el in enumerate(row):
            opt[i][j] = A[i][j]
            x[i][j] = j
    return x, opt


result = resource_allocation_task(A=np.array([[0, 1, 2, 3],
                                              [0, 0, 1, 2],
                                              [0, 2, 2, 3]]))

print('x:\n', result[0])
print('\nopt:\n', result[1])
print('\nallocated resources:', result[2])

