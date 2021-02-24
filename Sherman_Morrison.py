import numpy as np


def first_step(reverse_matrix, x_vector, index):
    # print('Вектор столбец x:', x_vector)
    L = np.dot(reverse_matrix, x_vector)
    # print('Вектор столбец L:', L)
    if L[index - 1] != 0:
        return L
    else:
        print('Матрица необратима')
        exit(0)


def second_step(l_vector, index):
    L_wave = l_vector.copy()
    L_wave[index - 1] = -1
    # print('L с волной:', L_wave)
    return L_wave


def third_step(l_vector, index, l_wave):
    scalar = -1. / l_vector[index - 1]
    L_roof = np.dot(scalar, l_wave)
    # print('L с домиком:', L_roof)
    return L_roof


def fourth_step(l_roof, index):
    one_matrix = np.eye(len(l_roof))
    one_matrix[:, index - 1] = l_roof
    Q = one_matrix
    # print('Q:\n', Q, '\n')
    return Q


def fifth_step(q_matrix, reverse_matrix):
    reverse_matrix_with_line = np.dot(q_matrix, reverse_matrix)
    # print('Обратная матрица с чертой:\n', reverse_matrix_with_line)
    return reverse_matrix_with_line


def get_reverse_matrix_with_line(reverse_matrix, x_vector, index):
    L_vector = first_step(reverse_matrix, x_vector, index)
    L_wave = second_step(L_vector, index)
    L_roof = third_step(L_vector, index, L_wave)
    Q = fourth_step(L_roof, index)
    reverse_matrix_with_line = fifth_step(Q, reverse_matrix)
    return reverse_matrix_with_line


# get_reverse_matrix_with_line(np.array([[1,  1, 0],
#                                        [0,  1,  0],
#                                        [0,    0,  1]]),
#                              np.array([1, 0, 1]),
#                              3)
