def topological_sort(g, start):
    if start not in g.keys():
        return None

    seen, stack, order, q = set(), [], [], [start]
    while q:
        v = q.pop()
        if v not in seen:
            seen.add(v)
            q.extend(g[v][0])
            while stack and v not in g[stack[-1]][0]:
                order.append(stack.pop())
            stack.append(v)
    return stack + order[::-1]


def find_possible_ways(graph, to_edge):
    possible_ways = []
    for k, v in graph.items():
        if to_edge in v[0]:
            index = v[0].index(to_edge)
            possible_ways.append([k, v[1][index]])
    return possible_ways


def find_max_way(graph, edge_from, edge_to):
    topological_list = topological_sort(graph, edge_from)  # пунк 1
    if edge_to not in topological_list or topological_list is None:
        return None  # пункт 2 -- нет вершины - нет ответа

    removed = list(set(graph.keys()) - set(topological_list))
    for el in removed:
        del graph[el]

    topological_list = topological_list[0:topological_list.index(edge_to) + 1]

    l = {}
    for i in topological_list:
        l[i] = 0

    prev = ['*']
    for i in range(0, len(topological_list) - 1):
        from_edge, to_edge, sums = topological_list[i], topological_list[i + 1], []
        for possible_way in find_possible_ways(graph, to_edge):
            sum = l[possible_way[0]] + possible_way[1]
            sums.append([sum, possible_way[0]])
        sums.sort()
        l[to_edge] = sums[-1][0]
        prev.append(sums[-1][1])

    path, l_keys = [], list(l.keys())
    current_key = l_keys[-1]
    while current_key != '*':
        path.append(current_key)
        index = l_keys.index(current_key)
        current_key = prev[index]
        del l_keys[index]

    path.reverse()
    max_weight = list(l.values())[-1]

    return max_weight, path


graph = {
    1: [[2, 4],   # вершины
        [1, 1]],  # веса
    2: [[4, 3],
        [2, 1]],
    3: [[6],
        [1]],
    4: [[5],
        [1]],
    5: [[3, 6],
        [2, 1]],
    6: [[],
        []],
    7: [[3],
        [1]]
}

# graph = {
#     1: [[2, 11],
#         [5, 6]],
#     2: [[11, 3],
#         [6, 7]],
#     3: [[4, 10],
#         [9, 2]],
#     4: [[5, 9],
#         [13, 3]],
#     5: [[6, 7],
#         [5, 3]],
#     6: [[],
#         []],
#     7: [[6],
#         [17]],
#     8: [[7],
#         [0]],
#     9: [[8, 5, 7],
#         [2, 3, 11]],
#     10: [[8, 9, 4],
#          [10, 12, 2]],
#     11: [[3, 10],
#          [2, 3]]
# }


result = find_max_way(graph, edge_from=1, edge_to=9)
print('Максимальный вес: ', result[0])
print('Оптимальный путь', result[1])
