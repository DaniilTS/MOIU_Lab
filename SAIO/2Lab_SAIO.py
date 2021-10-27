import math
import random
import numpy as np
from SimplexMethod import simplex_first_phase


# def gomori_method_recursion(A, b, A_first_len):
#     temp_A = np.array(np.copy(A))
#     x, Jb, not_Jb = simplex_first_phase(A, b)
#     if x is None:
#         return None
#
#     # x = np.around(x, 2)
#     # temp_A = np.around(temp_A, 3)
#     if x_is_suitable(x):
#         return x[:A_first_len]
#
#     not_int_indexes = get_not_int_indexes(x)
#     selected_index = random.choice(not_int_indexes)
#
#     Ab = basis_matrix(temp_A, Jb)
#     A_not_b = basis_matrix(temp_A, not_Jb)
#     Ab_inv = np.linalg.inv(Ab)
#     multi = np.array(Ab_inv.dot(A_not_b))
#
#     while selected_index >= multi.shape[0]:
#         selected_index = random.choice(not_int_indexes)
#
#     selected_row = multi[selected_index]
#
#     new_row = create_new_row(x, not_Jb, selected_row)
#     new_column = create_new_column(temp_A)
#     new_A = np.vstack([temp_A, new_row])
#     new_A = np.hstack([new_A, new_column])
#     new_b = np.hstack([b, get_fractional_part(x[selected_index])])
#
#     counter = counter + 1
#     return gomori_method_recursion(new_A, new_b, A_first_len)


def gomori_method_cycle(A, b, A_first_len):
    while True:
        x, Jb, not_Jb = simplex_first_phase(A, b)
        if x is None:
            return None

        if x_is_suitable(x):
            return x[:A_first_len]

        not_int_indexes = get_not_int_indexes(x)
        selected_el = random.choice(not_int_indexes)
        selected_index = not_int_indexes.index(selected_el)

        Ab = basis_matrix(A, Jb)
        A_not_b = basis_matrix(A, not_Jb)
        Ab_inv = np.linalg.inv(Ab)
        multi = np.array(Ab_inv.dot(A_not_b))

        selected_row = multi[selected_index]

        new_row = create_new_row(x, not_Jb, selected_row)
        new_column = create_new_column(A)
        A = np.vstack([A, new_row])
        A = np.hstack([A, new_column])
        b = np.hstack([b, get_fractional_part(x[selected_index])])


def get_fractional_part(num):
    left = math.floor(num)
    return num - left


def create_new_row(x, not_Jb, selected_row):
    new_row = []
    sel_index = 0
    for index, el in enumerate(x):
        if index + 1 in not_Jb:
            new_row.append(get_fractional_part(selected_row[sel_index]))
            sel_index = sel_index + 1
        else:
            new_row.append(0)

    return np.array(new_row)


def create_new_column(A):
    new_column = np.zeros(A.shape[0] + 1)
    new_column[-1] = -1

    res = []
    for el in new_column:
        res.append([el])

    return np.array(res)


def basis_matrix(a, jb):
    return np.array([[element for j, element in enumerate(row) if j + 1 in jb] for row in list(a)])


def get_not_int_indexes(x):
    not_integer_indexes = []
    for index, num in enumerate(x):
        if not np.round(num, 2).is_integer():
            not_integer_indexes.append(index)
    return not_integer_indexes


def x_is_suitable(x):
    for num in x:
        if not np.round(num, 2).is_integer():
            return False
    return True


result = gomori_method_cycle(A=np.array([[-4., 6., 1., 0.],
                                         [1., 1., 0., 1.]]),
                                 b=np.array([9., 4.]),
                                 A_first_len=4)


print(result)
