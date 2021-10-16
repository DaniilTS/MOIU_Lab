import numpy.linalg

a = [0, 0, 0]
b = [0, 0, 0]
C = [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]


def SZ_method(A, b):
    n = len(b)
    m = len(A)

    X = [[0] * n for _ in range(m)]
    i, j = 0, 0
    J_b = []

    while True:
        J_b.append((i, j))
        max_supply = min(A[i], b[j])
        A[i] -= max_supply
        b[j] -= max_supply
        X[i][j] = max_supply
        if i == m - 1 and j == n - 1:
            break
        if A[i] == 0 and i != len(A) - 1:
            i += 1
        elif b[j] == 0 and j != len(b) - 1:
            j += 1

    return X, J_b


def Get_VU(C, I_b):
    m = len(C)
    n = len(C[0])
    A = [[0] * (n + m) for _ in range(n + m)]
    b = [0] * (n + m)

    A[-1][0] = 1
    b[-1] = 0

    for it_num, (i, j) in enumerate(I_b):
        A[it_num][i] = A[it_num][m + j] = 1
        b[it_num] = C[i][j]

    x = numpy.linalg.solve(A, b)
    return x[:m], x[m:]


def new_Jb(m, n, J_b):
    J_bh, J_bv = [[] for _ in range(m)], [[] for _ in range(n)]

    for i, j in J_b:
        J_bh[i].append(j)
        J_bv[j].append(i)

    return J_bh, J_bv


def gen(n, m):
    for i in range(n):
        for j in range(m):
            yield i, j


def transport_task(a, b, C):
    m = len(a)
    n = len(b)

    print("\nУсловия баланса: ")
    difference = sum(a) - sum(b)
    if difference != 0:
        print("-")
        exit()
    else:
        print("+")

    print("\na: ", a)
    print("b:", b)
    print("c: ", C)

    X, J_b = SZ_method(a, b)
    print("Базисный план: ", X)
    print("Множество клеток: ", J_b)

    print("\nМетод потенциалов: ")
    iteration = 1
    while True:
        print("ИТЕРАЦИЯ ", iteration)
        u, v = Get_VU(C, J_b)

        for i, j in gen(m, n):
            if u[i] + v[j] > C[i][j]:
                J_b.append((i, j))
                break
        else:
            print("\nИтоговый оптимальный план перевозок: ")
            for i0 in range(m):
                for j0 in range(n):
                    print(X[i0][j0], end='\t')
                print()
            return
        print("\nРасширенное множество клеток: ", J_b)

        J_bh, J_bv = new_Jb(m, n, J_b)
        print("Клетки в местах, где цикл поворачивает на 90 градусов: ", J_bh)
        loop = [(i, j)]
        deleted = True

        while deleted:
            deleted = False
            for i, row in enumerate(J_bh):
                if len(row) < 2:
                    for j in row:
                        J_bv[j].remove(i)
                        deleted = True
                    row.clear()
            for j, column in enumerate(J_bv):
                if len(column) < 2:
                    for i in column:
                        J_bh[i].remove(j)
                        deleted = True
                    column.clear()
        up = True
        i, j = loop[0]

        while True:
            if up:
                up = False
                i = J_bv[j][1] if J_bv[j][0] == i else J_bv[j][0]
            else:
                up = True
                j = J_bh[i][1] if J_bh[i][0] == j else J_bh[i][0]
            if i == loop[0][0] and j == loop[0][1]:
                break
            else:
                loop.append((i, j))

        theta = min(X[loop[i][0]][loop[i][1]] for i in range(1, len(loop), 2))
        factor = 1

        for i, j in loop:
            X[i][j] += factor * theta
            if X[i][j] == 0 and len(J_b) > n + m - 1 and factor == -1:
                J_b.remove((i, j))
            factor = -1 if factor == 1 else 1
        print("Текущий план X: ", X)
        iteration += 1


transport_task(a, b, C)
