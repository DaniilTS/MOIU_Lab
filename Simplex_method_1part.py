# 25 Variant
import numpy as np
from Simplex_method_2part import simplex_method_second_part


def basis_matrix(a, jb):
    return [[element for j, element in enumerate(row) if j + 1 in jb] for row in list(a)]


def Jb_contains_indexes_more_n(Jb, n):
    for index, elem in enumerate(Jb):
        if elem > n:
            return True, index, elem
    return False, None, None


def simplex_method_first_part(A, b):
    m, n = A.shape

    for i, elem in enumerate(b):
        if elem < 0:
            A[i] = -1 * A[i]
            b[i] = -1 * elem

    E = np.identity(m)
    A_extended = np.concatenate((A, E), axis=1)
    x = np.concatenate((np.zeros(n), b), axis=0)
    c = np.array([0] * n + [-1] * m)
    artificial_Jb = np.array(range(n + 1, n + m + 1))
    optimal_plan, Jb = simplex_method_second_part(A_extended, b, c, x, artificial_Jb.tolist())
    artificial_Jb = [num - 1 for num in artificial_Jb]

    for i in artificial_Jb:
        if optimal_plan[i] != 0:
            return None, None, None

    size = len(optimal_plan)
    optimal_plan = np.delete(optimal_plan, range(size - m, size))

    J = list(range(1, n + 1))
    not_base_indexes = list(set(J) - set(Jb))

    counter = 0
    isTrue, index, j_k = Jb_contains_indexes_more_n(Jb, n)
    while isTrue:
        rel_index = j_k - n
        found = False
        for j in not_base_indexes:
            B = np.linalg.inv(basis_matrix(A_extended, Jb))
            alpha = B.dot(A[:, j - 1])
            if alpha[index] != 0:
                Jb[index] = j
                found = True
                break

        if not found:
            A = np.delete(A, rel_index)
            A_extended = np.delete(A_extended, rel_index)
            Jb.remove(Jb[index])
            counter = counter + 1

        isTrue, index, j_k = Jb_contains_indexes_more_n(Jb, n)

    for index, element in enumerate(optimal_plan):
        if element == 0 and counter != 0:
            optimal_plan = np.delete(optimal_plan, index)
            counter - 1
            break

    return optimal_plan, Jb, not_base_indexes


# print(simplex_method_first_part(A=np.array([[-4., 6., 1., 0., 0.],
#                                             [1., 1., 0., 1., 0.],
#                                             [0, 0, 0.1, 0.4, -1]]),
#                        b=np.array([9., 4., 0.5])))