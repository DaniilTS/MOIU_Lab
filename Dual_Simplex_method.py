import numpy as np

A = np.matrix([[1, -3, 1, 0],
               [-2, -1, 1, 1]])

b = np.matrix([[-3, -15]])
c = [0, -4, 1, 0]
Jb = [3, 4]


def dual_simplex_method(A, b, c, Jb):
    n = len(c)
    J_b = []
    for i in Jb:
        J_b.append(i - 1)
    A_b = A[:, J_b]
    B = np.linalg.inv(A_b)
    c_b = [c[i] for i in J_b]
    print("\nБазисный вектор с: ", c_b)
    dual_optimal_plan = (c_b * B).transpose()
    print("\nНачальный оптимальный план: ")
    print(dual_optimal_plan)

    iteration = 1
    while True:
        print("ИТЕРАЦИЯ ", iteration)
        print("\nБазисная матрица А: \n", A_b)
        print("\nОбратная базисная матрица B: \n", B)

        kappa_b = B * b
        print('Каппа:\n {}\n'.format(kappa_b.ravel().tolist()))

        kappa_plan = [0 if index not in J_b else kappa_b[J_b.index(index)].item(0) for index in range(n)]
        print('Каппа план: {}'.format(kappa_plan))

        negative_elements_indexes = [index for index in range(len(kappa_plan)) if kappa_plan[index] < 0]
        if len(negative_elements_indexes) == 0:
            break

        print('Индексы негативных переменных: {}'.format([i + 1 for i in negative_elements_indexes]))
        j_s = negative_elements_indexes[0]
        delta_y = B[J_b.index(j_s)]
        print("Двойственный план y': {}".format(delta_y))

        mu = get_negative_mus(J_b, n, delta_y, A)
        print('Мю: {}'.format(mu))

        j0, sigma0 = get_min_sigma_with_index(c, A, mu, dual_optimal_plan)
        print('Минимальная сигма: {}'.format(sigma0))

        print('j_0: {}'.format(j0))
        dual_optimal_plan = dual_optimal_plan + sigma0.item(0) * delta_y.transpose()
        print('y: {}'.format(dual_optimal_plan.ravel().tolist()))

        J_b[J_b.index(j_s)] = j0
        print('\nБазисные индексы: {}'.format(J_b))

        index = J_b.index(j0)
        B = get_reversed_matrix(A_b, B, A[:, j0], index)
        A_b[:, index] = A[:, j0]
        iteration = iteration + 1

    print("\n\nРезультат двойственного симлекс метода:")
    print("Оптимальный план: {}".format(kappa_plan))
    print("Базисные индексы: {}".format(J_b))


def get_reversed_matrix(A_b, B, vector, i):
    l = B * vector
    if l[i] == 0:
        return None

    li = l.item(i)
    l[i] = -1
    l_cap = -1 / li * l
    e = np.identity(len(A_b))
    e[:, i] = np.transpose(l_cap)
    reverse_matrix = e * B

    return reverse_matrix


def get_negative_mus(J_b, n, delta_y, A):
    J_n = [index for index in range(n) if index not in J_b]
    mu = [delta_y * A[:, index] for index in J_n]
    negative_indexes = [J_n[index] for index in range(len(mu)) if mu[index] < 0]

    if len(negative_indexes) == 0:
        print("Задача несовместна")
        exit(1)

    mu_with_indexes = {negative_indexes[index]: float(mu[index]) for index in range(len(negative_indexes))}
    return mu_with_indexes


def get_min_sigma_with_index(c, A, mu, dual_optimal_plan):
    sigmas = {index: (c[index] - A[:, index].transpose() * dual_optimal_plan) / mu_value for index, mu_value in mu.items()}
    print('\nВектор сигма: {}'.format(sigmas))

    min_sigma_index = min(sigmas, key=sigmas.get)
    return min_sigma_index, sigmas.get(min_sigma_index)


dual_simplex_method(A, b.transpose(), c, Jb)
