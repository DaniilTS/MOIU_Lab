# 25 Variant
import numpy as np
from Simplex_method_2part import simplex_method_second_part


def basis_matrix(a, jb):
    Ab = [[element for j, element in enumerate(row) if j + 1 in jb] for row in list(a)]
    return Ab


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

    print(A_extended)

    x = np.concatenate((np.zeros(n), b), axis=0)
    print('x:', x)

    c = np.array([0] * n + [-1] * m)
    print('c:', c)

    artificial_Jb = np.array(range(n + 1, n + m + 1))
    print('artificial_Jb:', artificial_Jb)

    optimal_plan, Jb = simplex_method_second_part(A_extended, b, c, x, artificial_Jb.tolist())
    print('Optimal plan:', optimal_plan)
    print('Jb of optimal plan:', Jb)

    artificial_Jb = [num - 1 for num in artificial_Jb]

    for i in artificial_Jb:
        if optimal_plan[i] != 0:
            print('Задача несовместна')
            return

    print('Задача совместна')

    size = len(optimal_plan)
    optimal_plan = np.delete(optimal_plan, range(size - m, size))  # удалили последние m элементов
    print(optimal_plan)

    J = list(range(1, n + 1))
    not_base_indexes = list(set(J) - set(Jb))
    print('не базисные индексы:', not_base_indexes)

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

        isTrue, index, j_k = Jb_contains_indexes_more_n(Jb, n)

    for index, element in enumerate(optimal_plan):
        if element == 0:
            optimal_plan = np.delete(optimal_plan, index)
            break

    return optimal_plan


print('Оптимальный план:', simplex_method_first_part(A=np.array([[-1., 5., 1., 0., 0.],
                                                                 [1., 1., 0., 1., 0.],
                                                                 [0., 6., 1., 1., 0.]]),
                                                     b=np.array([5., 4., 9.])))
# VAR 25
# [[-3., 7., 1, 0., 0.],
#  [7., 5., 0., 1., 0.],
#  [0., -1., 0., 0., 1.]]
# [14., 42., -4.]

#  VAR 19
# [[-1., 5., 1., 0., 0.],
#  [1., 1., 0., 1., 0.],
#  [0., 6., 1., 1., 0.]]
# [5., 4., 9.]
