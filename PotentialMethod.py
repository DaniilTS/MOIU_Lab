import numpy as np


def solve_transport_problem(supply_vector, applications_vector, cost_matrix):
    if sum(supply_vector) == sum(applications_vector):

        J = []
        for i in range(len(supply_vector)):
            for j in range(len(applications_vector)):
                J.append((i, j))

        x, Jb, Jb_elements = first_phase(supply_vector, applications_vector, cost_matrix)
        print('X:\n', x)
        print('Jb:\n', Jb)
        not_Jb = list(set(J) - set(Jb))

        return second_phase(x, J, Jb, not_Jb, Jb_elements, cost_matrix)

    else:
        print('условие баланса не выполнено, нет смысла решать задачу')
        return None


def first_phase(a, b, c):
    m, n = np.shape(c)

    x = np.zeros((m, n))
    Jb = []
    Jb_elements = []

    i = 0
    j = 0
    while True:
        if a[i] == 0 and b[j] == 0:
            break

        if a[i] == 0 or b[j] == 0:
            if a[i] == 0:
                i = i + 1
            else:
                j = j + 1

        minimum = min(a[i], b[j])
        Jb_elements.append(minimum)
        a[i] = a[i] - minimum
        b[j] = b[j] - minimum

        x[i, j] = minimum
        Jb.append((i, j))

    return x, Jb, Jb_elements


def second_phase(x, J, Jb, not_Jb, Jb_elements, c):
    while True:
        left_part = get_left_part(x, Jb)
        right_part = get_right_part(c, Jb)
        solution = np.linalg.solve(left_part, right_part)
        print('System solution:\n', solution)

        middle = int((len(solution) / 2))
        u = solution[0:middle]
        v = solution[middle:len(solution)]

        result, new_Jb_index = is_optimal_condition(c, u, v, not_Jb)
        if result:
            print('X:\n', x)
            return x

        Jb.insert(0, new_Jb_index)  # add new base position

        delete_extra_rows_columns(x, Jb)
        add_subtract_tau(Jb_elements)
        print('индексы базисных элементов:', Jb)

        m, n = x.shape

        for index, elem in enumerate(Jb_elements):
            if elem == 0:
                Jb_elements.pop(index)
                Jb.pop(index)
                break

        print('элементы на базисных индексах:', Jb_elements)
        print('базисные индексы:', Jb)

        counter = 0
        for i in range(n):
            for j in range(m):
                if (i, j) in Jb:
                    x[i, j] = Jb_elements[counter]
                    counter = counter + 1
                else:
                    x[i, j] = 0
        print(x)

        not_Jb = list(set(J) - set(Jb))


def get_left_part(x, Jb):
    m, n = x.shape
    left_part = np.zeros((m * 2, n * 2), dtype=float)

    row = 0
    for i, j in Jb:
        left_part[row, i] = 1.
        left_part[row, j + n] = 1.
        row = row + 1

    left_part[row, 0] = 1.
    print('Left part: \n', left_part)
    return left_part


def get_right_part(c, Jb):
    right_part = []
    for i, j in Jb:
        right_part.append(c[i, j])

    right_part.append(0)
    right_part = np.array(right_part, dtype=float)
    print('Right part:\n', right_part)
    return right_part


def is_optimal_condition(c, u, v, not_Jb):
    for i, j in not_Jb:
        if u[i] + v[j] > c[i, j]:
            return False, (i, j)
    return True


def delete_extra_rows_columns(x, Jb):
    m, n = x.shape
    counter = 0
    for i in range(m):
        for j in range(n):
            if (i, j) in Jb:
                counter = counter + 1
        if counter > 0:
            counter = 0
        else:
            x = np.delete(x, i, axis=0)

    counter = 0
    for i in range(m):
        for j in range(n):
            if (j, i) in Jb:
                counter = counter + 1
        if counter > 0:
            counter = 0
        else:
            x = np.delete(x, i, axis=1)

    print('new X:\n', x)


def add_subtract_tau(Jb_elements):
    tau = np.amin(Jb_elements)
    Jb_elements.insert(0, 0)

    minus = -1
    for i in range(len(Jb_elements)):
        Jb_elements[i] = Jb_elements[i] - (tau * minus)
        minus = minus * -1

    print('новые элементы на базисных индексах:', Jb_elements)


print(solve_transport_problem(supply_vector=[100, 300, 300],
                        applications_vector=[300, 200, 200],
                        cost_matrix=np.array([[8, 4, 1],
                                              [8, 4, 3],
                                              [9, 7, 5]])))
