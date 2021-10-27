from scipy.optimize import linprog
import numpy as np


class ILP_Task:
    def __init__(self, A, B):
        self.A = A
        self.B = B


def branch_and_bound_method(A, B, c):
    record = -np.inf
    x = []
    stack = [ILP_Task(A, B)]
    counter = 0

    while len(stack) > 0 and counter < np.inf:
        counter += 1
        task = stack.pop()
        task_res = linprog(c, task.A, task.B)

        if not task_res.success:
            continue

        if task_res.success:
            ilp_x = []
            not_int_x = None

            for xx in task_res.x:
                ilp_x.append(round(xx, 2))

            for xx in ilp_x:
                if not int(xx) == xx:
                    i = ilp_x.index(xx)
                    not_int_x = xx

            new_record = int(sum([c[i] * ilp_x[i] for i in range(len(c))]))
            if new_record <= record:
                continue

            if not not_int_x:
                record = new_record
                x = ilp_x
                continue

            rounded_not_int = int(not_int_x)
            x1, x2 = [[0 for i in range(len(c))]], [[0 for i in range(len(c))]]
            x1[0][i], x2[0][i] = 1, -1
            new_ILP_left = ILP_Task(np.concatenate((task.A, x1)), np.concatenate((task.B, [rounded_not_int])))
            new_ILP_right = ILP_Task(np.concatenate((task.A, x2)), np.concatenate((task.B, [rounded_not_int + 1])))

            stack.append(new_ILP_right)
            stack.append(new_ILP_left)
    return x


print('Ответ', branch_and_bound_method(A=np.array([[4, 3],
                                                   [-4, 3]]),
                                       B=np.array([22, 2]),
                                       c=np.array([5, -4])))
