import copy as cp
import numpy as np


def fill_list(lst, length):
    for i in range(length):
        lst.append(None)


def fill_U_V(U, V, C, Jb, Jb2):
    U[0] = 0
    while True:
        for j in Jb:
            f_i = j[0] - 1
            s_i = j[1] - 1
            if (U[f_i] is not None) and (V[s_i] is None):
                V[s_i] = C[f_i][s_i] - U[f_i]
                Jb2.remove(j)
            elif (U[f_i] is None) and (V[s_i] is not None):
                U[f_i] = C[f_i][s_i] - V[s_i]
                Jb2.remove(j)
        if (not Jb2) or (None not in V) and (None not in U):
            break


def fill_list_on_indexes(lst, length):
    for i in range(length):
        if lst[i] is None:
            lst[i] = 0


def mark_calc(M, N, U, V, X, C, Jb):
    flag = []
    k = 0
    for i in range(M):
        for j in range(N):
            if [i + 1, j + 1] in Jb:
                continue

            delta = U[i] + V[j] - C[i][j]

            if (delta > 0) and (X[i][j] == 0) or (delta < 0) and (X[i][j] == 10):
                flag = [delta, i + 1, j + 1]
                if X[i][j] == 0:
                    k = 1
                elif X[i][j] == 10:
                    k = -1
                break
        if k != 0:
            break

    return k, flag


def add_to_basis_indexes(Jb, mark, N):
    m1 = mark[1]
    m2 = mark[2]

    if (Jb[0][0] == m1) and (Jb[-1][1] == m2):
        Jb.append([m1, m2])
    else:
        stop, coef = list(), None
        for i in range(1, N + 1):
            if [m1, i] in Jb:
                if coef is None:
                    if not stop:
                        stop = Jb[Jb.index([m1, i]) - 1]
                    if stop[1] <= m2:
                        coef = i
                elif abs(i - coef) > abs(m2 - i):
                    coef = i
        if coef is None:
            for i in range(m1 - 1, 0, -1):
                if [i, m2] in Jb:
                    coef = i
                    break
            if coef is None:
                coef = 0
                for j in range(m2, N + 1):
                    if [1, j] in Jb:
                        coef = Jb.index([1, j])
                Jb.insert(coef, [m1, m2])
            else:
                Jb.insert(Jb.index([coef, m2]) + 1, [m1, m2])
        else:
            Jb.insert(Jb.index([m1, coef]), [m1, m2])


def Jb_tweak(Jb2):
    for i in range(len(Jb2) - 1):
        for j in range(i + 1, len(Jb2)):
            if (Jb2[i][0] == Jb2[j][0]) or (Jb2[i][1] == Jb2[j][1]):
                if j - i == 1:
                    break
                else:
                    delta = Jb2[j]
                    Jb2.remove(delta)
                    Jb2.insert(i + 1, delta)


def set_neg_pos_start(Jb2, mark, k):
    neg_num_start, pos_num_start = Jb2.index([mark[1], mark[2]]), 0
    if neg_num_start % 2 == 0:
        pos_num_start = 1
    if k == -1:
        if pos_num_start == 1:
            pos_num_start = 0
        else:
            pos_num_start = 1
    return neg_num_start, pos_num_start


def update_plan(k, Jb2, neg_num_start, X, Min):
    if k == 1:
        return build_new_plan(Jb2, neg_num_start, X, Min, 1)
    else:
        return build_new_plan(Jb2, neg_num_start, X, Min, -1)


def build_new_plan(Jb2, neg_num_start, X, Min, val):
    for i, j in enumerate(Jb2):
        f_i = j[0] - 1
        s_i = j[1] - 1
        if i % 2 == neg_num_start % 2:
            X[f_i][s_i] += val * Min[0]
        else:
            X[f_i][s_i] -= val * Min[0]
    return X


def delete_rows(Jb2, del_lst, X2, N, flag):
    elements = [j[0] for j in Jb2]
    bad_elem = [item for item in elements if elements.count(item) <= 1]
    bad_elem.sort()
    bad_elem = bad_elem[::-1]
    for i in bad_elem:
        delete = len([x for x in del_lst if x < i])
        X2 = np.delete(X2, i - 1 - delete, axis=0)
        for j in range(1, N + 1):
            if [i, j] in Jb2:
                Jb2.remove([i, j])
    if not bad_elem:
        flag = True
    else:
        del_lst.update(bad_elem)

    return flag, del_lst


def delete_cols(Jb2, del_lst, X2, M, flag):
    elements = [j[1] for j in Jb2]
    bad_elem = [item for item in elements if elements.count(item) <= 1]
    bad_elem.sort()
    bad_elem = bad_elem[::-1]
    for i in bad_elem:
        delete = len([y for y in del_lst if y < i])
        X2 = np.delete(X2, i - 1 - delete, axis=1)
        for j in range(1, M + 1):
            if [j, i] in Jb2:
                Jb2.remove([j, i])
    if not bad_elem:
        flag = True
    else:
        del_lst.update(bad_elem)

    return flag, del_lst


def find_min(pos_num_start, Jb2, X):
    Min = list()
    for i in range(pos_num_start, len(Jb2), 2):
        delta = X[Jb2[i][0] - 1][Jb2[i][1] - 1]
        if delta == 0:
            continue
        if (not Min) or (delta <= Min[0]):
            Min = [delta, Jb2[i][0], Jb2[i][1]]

    if pos_num_start == 1:
        return count_min_values(pos_num_start, Jb2, X, Min, -1)
    else:
        return count_min_values(pos_num_start, Jb2, X, Min, 1)


def update_J(Min, flag, Jb):
    if [Min[1], Min[2]] != [flag[1], flag[2]]:
        Jb.remove([Min[1], Min[2]])
    else:
        Jb.remove([flag[1], flag[2]])


def count_min_values(start_pos, Jb_copy, X, Min, val):
    for i in range(start_pos + val, len(Jb_copy), 2):
        delta = 10 - X[Jb_copy[i][0] - 1][Jb_copy[i][1] - 1]
        if delta == 0:
            continue
        if (not Min) or (delta < Min[0]):
            Min = [delta, Jb_copy[i][0], Jb_copy[i][1]]
    return Min


def transport_task(C, X, M, N, Jb):
    iteration = 1
    while True:
        print('\nIteration:', iteration)

        U, V = list(), list()
        fill_list(U, M)
        fill_list(V, N)

        Jb2 = cp.copy(Jb)
        fill_U_V(U, V, C, Jb, Jb2)
        print('U:', U, '\n V:', V)

        k, mark = mark_calc(M, N, U, V, X, C, Jb)
        if not mark:
            print('\n *********STOP*********\n', X)
            return X

        add_to_basis_indexes(Jb, mark, N)

        X2, Jb2 = cp.copy(X), cp.copy(Jb)
        row_f = column_f = False
        x_delete = y_delete = set()
        while not row_f or not column_f:
            row_f, x_delete = delete_rows(Jb2, x_delete, X2, N, row_f)
            column_f, y_delete = delete_cols(Jb2, y_delete, X2, M, column_f)

        print('angle matrix:\n', X2)

        Jb_tweak(Jb2)
        neg_num_start, pos_num_start = set_neg_pos_start(Jb2, mark, k)

        Min = find_min(pos_num_start, Jb2, X)
        print('teta_min =', Min[0], 'on index', (Min[1], Min[2]))

        X = update_plan(k, Jb2, neg_num_start, X, Min)
        print('new plan:\n', X)

        update_J(Min, mark, Jb)
        print('new basis:\n', Jb)

        iteration += 1


transport_task(C=np.array([[1, 1, 20, -4, 15, -1],
                           [10, -5, -3, 1, -1, 2],
                           [-1, 2, 4, -5, 2, 1],
                           [4, 3, 40, 6, -6, -20],
                           [5, 10, -10, -3, 15, 5]]),

               X=np.array([[4, 3, 10, 0, 10, 0],
                           [10, 0, 0, 2, 0, 10],
                           [0, 0, 6, 0, 5, 9],
                           [0, 0, 10, 7, 0, 0],
                           [10, 5, 0, 0, 10, 4]]),
               M=5,
               N=6,
               Jb=[[1, 1], [1, 2], [2, 4], [3, 3], [3, 5], [3, 6], [4, 4], [4, 6], [5, 2], [5, 6]])
