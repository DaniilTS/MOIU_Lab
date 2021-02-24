import numpy as np
import random
from Sherman_Morrison import get_reverse_matrix_with_line

# ВАРИАНТ 25
A = np.array([[1, -1, 0, 2, -1, -1, 2, 1, 7],
              [-1, 2, 1, 3, 0, 1, 1, 1, 1],
              [1, -1, 1, 0, 1, 4, 4, 1, 2],
              [1, -3, 0, -8, 2, 3, 0, 1, 1]])

c = np.array([4, 1, 1, 3, 1, 4, 1, 1, -1])
b = np.array([15, 7, -8, 7], dtype=float)
x = np.array([0, 1, 0, 0, 0, 5, 1, 2, 0], dtype=float)
J = list(range(1, len(x) + 1))
Jb = [2, 6, 7, 8]
not_base_indexes = list(set(J) - set(Jb))


def recount_not_base_indexes():
    return list(set(J) - set(Jb))


def get_base_matrix():
    base_matrix = np.zeros(shape=(len(Jb), len(Jb)))
    for index in range(len(Jb)):
        base_matrix[:, index] = A.swapaxes(0, 1)[Jb[index] - 1, :]

    return base_matrix


def get_reverse_base_matrix_first_iter(base_matrix):
    return np.linalg.inv(base_matrix)


def get_Cb():
    return np.array([c[i - 1] for i in Jb])


def get_U(cb, reverse_matrix):
    return np.dot(cb, reverse_matrix)


def get_delta(u):
    left = np.dot(u, A)
    delta = left - c
    return delta


def get_not_base_deltas(delta_array):
    not_base_deltas = []
    for i in not_base_indexes:
        not_base_deltas.append(delta_array[i - 1])

    return not_base_deltas


def is_optimal_by_deltas(not_base_deltas):
    if all(delta >= 0 for delta in not_base_deltas):
        return True
    else:
        return False


def get_j_zero():
    return random.choice(not_base_indexes)


def get_vector_z(reverse_matrix, j_zero):
    return np.dot(reverse_matrix, A.swapaxes(0, 1)[j_zero - 1])


def get_tau_zero(z):
    tau_arr = []
    for i in range(len(Jb)):
        if z[i] > 0:
            tau_arr.append(round(x[Jb[i] - 1] / z[i], 4))
        else:
            tau_arr.append(np.inf)
    # print('массив tau:', tau_arr)

    tau_zero = min(tau_arr)
    if tau_zero == np.inf:
        print('Оптимального плана нет')
        print('Массив tau:', tau_arr)
        exit(0)

    tau_zero_index = tau_arr.index(tau_zero) + 1

    return tau_zero, tau_zero_index


def change_Jb_indexes(j_zero, tau_zero_index):
    changed_base_index = Jb[tau_zero_index - 1]
    Jb[tau_zero_index - 1] = j_zero
    # print(Jb)
    not_base_indexes = recount_not_base_indexes()
    # print(not_base_indexes)

    return changed_base_index


def recount_x_vector(j_zero, tau_zero, z, changed_jb_index):
    x[j_zero - 1] = tau_zero

    for num in Jb:
        if num != j_zero:
            num_index = Jb.index(num)
            x[num - 1] = x[num - 1] - tau_zero * z[num_index]

    x[changed_jb_index - 1] = 0


def first_iter():
    base_matrix = get_base_matrix()
    print('Базовая матрица:\n', base_matrix)

    reverse_matrix = get_reverse_base_matrix_first_iter(base_matrix)
    print('Обратная матрица:\n', reverse_matrix)

    Cb = get_Cb()
    print('Вектор компонент стоимостей:', Cb)

    u = get_U(Cb, reverse_matrix)
    print('Вектор потенциалов: ', u)

    delta = get_delta(u)
    print('Вектор оценок:', delta)

    not_base_deltas = get_not_base_deltas(delta)
    print('Дельты на небазисных индексах:', not_base_deltas)

    if is_optimal_by_deltas(not_base_deltas):
        print('Текущий базисный план оптимальный:', x)
        return None, None, None

    j_zero = get_j_zero()
    print('j0:', j_zero)

    z = get_vector_z(reverse_matrix, j_zero)
    print('Вектор z:', z)

    tau_zero, tau_zero_index = get_tau_zero(z)
    print(tau_zero, tau_zero_index)

    changed_Jb_index = change_Jb_indexes(j_zero, tau_zero_index)

    recount_x_vector(j_zero, tau_zero, z, changed_Jb_index)
    print('Новый вектор х:', x)

    x_vector = A.swapaxes(0, 1)[j_zero - 1]

    return reverse_matrix, x_vector, tau_zero_index


def another_iteration(reverse_matrix, x_vector, i):
    reverse_matrix = get_reverse_matrix_with_line(reverse_matrix, x_vector, i)
    Cb = get_Cb()
    u = get_U(Cb, reverse_matrix)
    delta = get_delta(u)
    not_base_deltas = get_not_base_deltas(delta)

    if is_optimal_by_deltas(not_base_deltas):
        print('\nТекущий базисный план оптимальный:', x)
        return None, None, None

    j_zero = get_j_zero()
    z = get_vector_z(reverse_matrix, j_zero)
    tau_zero, tau_zero_index = get_tau_zero(z)
    changed_Jb_index = change_Jb_indexes(j_zero, tau_zero_index)
    recount_x_vector(j_zero, tau_zero, z, changed_Jb_index)
    x_vector = A.swapaxes(0, 1)[j_zero - 1]

    return reverse_matrix, x_vector, tau_zero_index


def simplex_method_second_part():
    reverse_matrix, x_vector, i = first_iter()
    iteration = 1
    while True:
        reverse_matrix, x_vector, i = another_iteration(reverse_matrix, x_vector, i)
        if all(item is None for item in [reverse_matrix, x_vector, i]):
            print('Номер итерации:', iteration)
            return x
        iteration = iteration + 1


simplex_method_second_part()
