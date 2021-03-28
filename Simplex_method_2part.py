import numpy as np
from Sherman_Morrison import get_reverse_matrix_with_line

# ВАРИАНТ 25


def get_base_matrix(Jb, A):
    base_matrix = np.zeros(shape=(len(Jb), len(Jb)))
    for index in range(len(Jb)):
        base_matrix[:, index] = A.swapaxes(0, 1)[Jb[index] - 1, :]

    return base_matrix


def get_reverse_base_matrix_first_iter(base_matrix):
    return np.linalg.inv(base_matrix)


def get_Cb(c, Jb):
    return np.array([c[i - 1] for i in Jb])


def get_U(cb, reverse_matrix):
    return np.dot(cb, reverse_matrix)


def get_delta(u, A, c):
    left = np.dot(u, A)
    delta = left - c
    return delta


def get_not_base_deltas(delta_array, not_base_indexes):
    not_base_deltas = []
    for i in not_base_indexes:
        not_base_deltas.append(delta_array[i - 1])

    return not_base_deltas


def is_optimal_by_deltas(not_base_deltas):
    if all(delta >= 0 for delta in not_base_deltas):
        return True
    else:
        return False


def get_j_zero(delta, not_base_deltas):
    negative_num = get_first_neg(not_base_deltas)
    return delta.index(negative_num) + 1


def get_first_neg(array):
    for elem in array:
        if elem < 0:
            return elem


def get_vector_z(reverse_matrix, j_zero, A):
    return np.dot(reverse_matrix, A.swapaxes(0, 1)[j_zero - 1])


def get_tau_zero(z, Jb, x):
    tau_arr = []
    for i in range(len(Jb)):
        if z[i] > 0:
            tau_arr.append(round(x[Jb[i] - 1] / z[i], 4))
        else:
            tau_arr.append(np.inf)
    print('массив tau:', tau_arr)

    tau_zero = min(tau_arr)
    if tau_zero == np.inf:
        print('Оптимального плана нет')
        print('Массив tau:', tau_arr)
        exit(0)

    tau_zero_index = tau_arr.index(tau_zero) + 1

    return tau_zero, tau_zero_index


def change_Jb_indexes(j_zero, tau_zero_index, J, Jb):
    changed_base_index = Jb[tau_zero_index - 1]
    Jb[tau_zero_index - 1] = j_zero
    print("Новый Jb:", Jb)
    not_base_indexes = recount_not_base_indexes(J, Jb)
    print("не базисные индексы:", not_base_indexes)

    return changed_base_index, not_base_indexes


def recount_x_vector(j_zero, tau_zero, z, changed_jb_index, x, Jb):
    x[j_zero - 1] = tau_zero

    for num in Jb:
        if num != j_zero:
            num_index = Jb.index(num)
            x[num - 1] = x[num - 1] - tau_zero * z[num_index]

    x[changed_jb_index - 1] = 0


def first_iter(A, b, c, x, J, Jb, not_base_indexes):
    base_matrix = get_base_matrix(Jb, A)
    print('Базовая матрица:\n', base_matrix)

    reverse_matrix = get_reverse_base_matrix_first_iter(base_matrix)
    print('Обратная матрица:\n', reverse_matrix)

    Cb = get_Cb(c, Jb)
    print('Вектор компонент стоимостей:', Cb)

    u = get_U(Cb, reverse_matrix)
    print('Вектор потенциалов: ', u)

    delta = get_delta(u, A, c)
    print('Вектор оценок:', delta)

    not_base_deltas = get_not_base_deltas(delta, not_base_indexes)
    print('Дельты на небазисных индексах:', not_base_deltas)

    if is_optimal_by_deltas(not_base_deltas):
        return None, None, None, None, None, None, x, None, None

    j_zero = get_j_zero(delta.tolist(), not_base_deltas)
    print('j0:', j_zero)

    z = get_vector_z(reverse_matrix, j_zero, A)
    print('Вектор z:', z)

    tau_zero, tau_zero_index = get_tau_zero(z, Jb, x)
    print("Тау 0:", tau_zero, " Индеус тау 0:", tau_zero_index)

    changed_Jb_index, not_base_indexes = change_Jb_indexes(j_zero, tau_zero_index, J, Jb)

    recount_x_vector(j_zero, tau_zero, z, changed_Jb_index, x, Jb)
    print('Новый вектор х:', x)

    x_vector = A.swapaxes(0, 1)[j_zero - 1]

    return reverse_matrix, x_vector, tau_zero_index, A, b, c, x, Jb, not_base_indexes


def another_iteration(reverse_matrix, x_vector, i, A, b, c, x, J, Jb, not_base_indexes):
    reverse_matrix = get_reverse_matrix_with_line(reverse_matrix, x_vector, i)
    print("Обратная матрица:\n", reverse_matrix)
    Cb = get_Cb(c, Jb)
    print('Вектор компонент стоимостей:', Cb)
    u = get_U(Cb, reverse_matrix)
    print('Вектор потенциалов: ', u)
    delta = get_delta(u, A, c)
    print('Вектор оценок:', delta)
    not_base_deltas = get_not_base_deltas(delta, not_base_indexes)
    print('Дельты на небазисных индексах:', not_base_deltas)

    if is_optimal_by_deltas(not_base_deltas):
        return None, None, None, None, None, None, x, None, None

    j_zero = get_j_zero(delta.tolist(), not_base_deltas)
    print('j0:', j_zero)
    z = get_vector_z(reverse_matrix, j_zero, A)
    print('Вектор z:', z)
    tau_zero, tau_zero_index = get_tau_zero(z, Jb, x)
    changed_Jb_index, not_base_indexes = change_Jb_indexes(j_zero, tau_zero_index, J, Jb)
    recount_x_vector(j_zero, tau_zero, z, changed_Jb_index, x, Jb)
    print('Новый вектор х:', x)
    x_vector = A.swapaxes(0, 1)[j_zero - 1]

    return reverse_matrix, x_vector, tau_zero_index, A, b, c, x, Jb, not_base_indexes


def simplex_method_second_part(A, b, c, x, Jb):
    J = list(range(1, len(x) + 1))
    not_base_indexes = recount_not_base_indexes(J, Jb)
    print("Не базисные индексы:", not_base_indexes)

    reverse_matrix, x_vector, i, A, b, c, x, Jb, not_base_indexes = first_iter(A, b, c, x, J, Jb, not_base_indexes)
    iteration = 2

    while True:
        print("\nитерация: ", iteration)
        reverse_matrix, x_vector, i, A, b, c, x, Jb, not_base_indexes = another_iteration(reverse_matrix, x_vector, i, A, b, c, x, J, Jb, not_base_indexes)
        if all(item is None for item in [reverse_matrix, x_vector, i]):
            print('\nНомер итерации:', iteration + 1)
            print('Оптимальный базисный план: ', x)
            return x
        iteration = iteration + 1


def recount_not_base_indexes(J, Jb):
    return list(set(J) - set(Jb))


simplex_method_second_part(A=np.array([[3, 1, 1, 0, 0, 0],
                                       [1, 4, 0, 1, 0, 0],
                                       [1, 0, 0, 0, 1, 0],
                                       [0, 1, 0, 0, 0, 1]]),
                           b=np.array([30, 32, 9, 7]),
                           c=np.array([33, 21, 1, 0, 0, 0]),
                           x=np.array([0, 0, 30, 32, 9, 7]),
                           Jb=[3, 4, 5, 6])
