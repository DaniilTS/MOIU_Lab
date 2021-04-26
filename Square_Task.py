import numpy as np


def square_task(A, c, x, D, J, Je):
    while True:
        Ab_1, ux, deltax = get_Ab1_uX_deltaX(x, c, D, A)

        j0 = None
        for index, i in enumerate(deltax):
            if i < 0:
                j0 = index
                break
        if j0 is None:
            print("\nНовый  план new_x:\n {}".format(x))
            print("Обновленый вектор J:\n {}".format(J))
            print("Обновленый вектор Je:\n {}".format(Je))
            return
        print("j0:\n {}".format(j0))

        H_1 = build_H_1_Matrix(A, Je)
        vector_b = build_vector_b(j0, H_1)
        l = build_vector_l(j0, vector_b, c, Je)
        beta = get_beta(l)
        index_teta, x = get_teta_and_new_x(l, x, beta, deltax, j0)

        # Обновляем опорный план
        ########################## first_check ##########################
        flag = 0
        for j in J:
            if j in Je:
                flag += 1
        if flag == len(J) and flag == len(Je):
            pass

        if j0 == index_teta - 1:
            Je = np.append(Je, index_teta)
            print("Обновленый вектор J:\n {}".format(J))
            print("Обновленый вектор Je:\n {}".format(Je))
            continue
        ########################## first_check ##########################

        ########################## second_check ##########################
        Js = []
        for j in Je:
            if j not in J:
                Js.append(j)
        if index_teta in Js:
            s = np.where(Je == index_teta)[0][0]
            Je = np.delete(Je, s)
            print("Обновленый вектор J:\n {}".format(J))
            print("Обновленый вектор Je:\n {}".format(Je))
            continue
        ########################## second_check ##########################

        ########################## third_check ##########################
        if index_teta in J:
            s = np.where(Je == index_teta)[0][0]
            flag = 0
            for jp in Js:
                res = Ab_1.dot(A[:, jp - 1])
                if res[s] != 0:
                    flag = jp

            if flag != 0:
                for index, k in enumerate(J):
                    if k == index_teta:
                        J[index] = jp
                        break
                for index, k in enumerate(Je):
                    if k == index_teta:
                        Je = np.delete(Je, index)
                        break
                J = np.sort(J)
                Je = np.sort(Je)
                print("Обновленый вектор J:\n {}".format(J))
                print("Обновленый вектор Je:\n {}".format(Je))
                continue
        ########################## third_check ##########################

        ########################## fourth_check ##########################
        if index_teta in J:
            flag = 0
            for j in J:
                if j in Je:
                    flag += 1

            if flag == len(J) and flag == len(Je):
                s = np.where(J == index_teta)[0][0]
                J[s] = j0 + 1
                s = np.where(Je == index_teta)[0][0]
                Je[s] = j0 + 1
                print("Обновленый вектор J:\n {}".format(J))
                print("Обновленый вектор Je:\n {}".format(Je))
                continue

            s = np.where(Je == index_teta)[0][0]
            flag = 0
            for jp in Js:
                res = Ab_1.dot(A[:, jp - 1])
                if res[s] == 0:
                    flag = 1

            if flag == 1:
                s = np.where(J == index_teta)[0][0]
                J[s] = j0 + 1
                s = np.where(Je == index_teta)[0][0]
                Je[s] = j0 + 1
                print("Обновленый вектор J:\n {}".format(J))
                print("Обновленый вектор Je:\n {}".format(Je))
                continue
        ########################## fourth_check ##########################


def get_Ab1_uX_deltaX(x, c, D, A):
    # Подсчитываем с u delta
    cx = c + x.dot(D)
    print("Вектор c(x):\n {}".format(cx))
    Ab = []
    cxb = []
    for ji in J:
        Ab.append(A[:, ji - 1])
        cxb.append(cx[ji - 1])
    Ab = np.array(Ab).transpose()
    Ab_1 = np.linalg.inv(Ab)
    cxb = np.array(cxb)
    ux = -1 * cxb.dot(Ab_1)
    print("Вектор u(x):\n {}".format(ux))
    deltax = ux.dot(A) + cx
    for index, i in enumerate(deltax):
        if abs(i) < 0.0000000001:
            deltax[index] = 0
    print("Вектор delta(x):\n {}".format(deltax))
    return Ab_1, ux, deltax


def build_vector_l(j0, x_row, c, Je):
    # строим вектор l
    l = np.zeros(len(c))
    l[j0] = 1
    for index, i in enumerate(Je):
        l[i - 1] = x_row[index]
    print("Вектор l:\n {}".format(l))
    return l


def get_beta(l):
    # находи beta
    beta = (l.dot(D)).dot(np.transpose(l))
    print("Вектор beta:\n {}".format(beta))
    return beta


def build_vector_b(j0, H_1):
    # Строим вектор в для ветора l
    be = []
    for i in Je:
        be.append(D[i - 1][j0])
    for i in range(len(A)):
        be.append(A[i][j0])
    be = np.array(be)
    print("Вектор b*:\n {}".format(be))
    x_row = -1 * H_1.dot(be)
    print("Вектор x^:\n {}".format(x_row))
    return x_row


def build_H_1_Matrix(A, Je):
    # Строим матрицу Н
    Abe = []
    for ji in Je:
        Abe.append(A[:, ji - 1])
    Abe = np.array(Abe).transpose()
    Abe_1 = Abe.transpose()
    De = []
    for i in Je:
        temp = []
        for j in Je:
            temp.append(D[j - 1][i - 1])
        De.append(temp)
    De = np.array(De)
    cc = np.concatenate((De, Abe_1), axis=1)
    bb = np.concatenate((Abe, np.zeros((len(Abe), len(Abe_1[0]) + len(De[0]) - len(Abe[0])))), axis=1)
    H = np.concatenate((cc, bb), axis=0)
    print("Матрица H:\n {}".format(H))
    H_1 = np.linalg.inv(H)
    print("Матрица H-1:\n {}".format(H_1))
    return H_1


def get_teta_and_new_x(l, x, beta, deltax, j0):
    # находим teta и мин значение(если такое существует)
    teta = []
    for index, i in enumerate(Je):
        if l[i - 1] >= 0:
            teta.append(np.inf)
        else:
            teta.append(-1 * x[i - 1] / l[i - 1])
    tetaj0 = None
    if beta == 0:
        tetaj0 = np.isfinite
    else:
        tetaj0 = abs(deltax[j0] / beta)
    print("Вектор teta:\n {}".format(teta))
    print("Вектор tetaj0:\n {}".format(tetaj0))

    teta0 = np.minimum(np.amin(teta), tetaj0)
    if not np.isfinite(teta0):
        return "Целевая функция неограниченна снизу"
    index_teta = None
    if teta0 == tetaj0:
        index_teta = j0 + 1
    else:
        index_teta = Je[np.where(teta == teta0)[0][0]]
    print("Индекс минимального тета index_teta:\n {}".format(index_teta))
    x = x + teta0 * l
    print("Новый  план new_x:\n {}".format(x))
    return index_teta, x


if __name__ == "__main__":
    # Variant 15
    A = np.array([[3, 3, 0], [3, 0, 1]])
    c = np.array([-1, -1, -1])
    D = np.array([[4, -1, 0], [-1, 1, 0], [0, 0, 1]])
    X = np.array([0, 7 / 3, 3])
    J = np.array([2, 3])
    Je = np.array([2, 3])

    # Variant 10
    # A = np.array([[0, 4, 1], [1, 0, 3]])
    # c = np.array([0, 0, -1])
    # D = np.array([[1, 0, 0], [0, 4, -2], [0, -2, 4]])
    # X = np.array([1, 0.25, 0])
    # J = np.array([1, 2])
    # Je = np.array([1, 2])

    square_task(A, c, X, D, J, Je)
