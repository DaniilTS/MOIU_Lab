# from collections import defaultdict
#
#
# class Graph:
#     def __init__(self, vertices):
#         self.graph = defaultdict(list)
#         self.V = vertices
#
#     def addEdge(self, u, v):
#         self.graph[u].append(v)
#
#     def topologicalSortUtil(self, v, visited, stack):
#         visited[v] = True
#
#         for i in self.graph[v]:
#             if not visited[i]:
#                 self.topologicalSortUtil(i, visited, stack)
#
#         stack.insert(0, v)
#
#     def topologicalSort(self, startPosition):
#         visited = [False] * self.V
#         stack = []
#
#         for i in range(self.V):
#             if not visited[i]:
#                 self.topologicalSortUtil(i, visited, stack)
#
#         print(stack)
#
#
# g = Graph(7)
# g.addEdge(1, 2)
# g.addEdge(1, 4)
# g.addEdge(2, 4)
# g.addEdge(2, 3)
# g.addEdge(5, 3)
# g.addEdge(5, 6)
# g.addEdge(3, 6)
# g.addEdge(7, 3)
#
# g.topologicalSort()


def iterative_topological_sort(graph, start):
    seen = set()
    stack = []
    order = []
    q = [start]
    while q:
        v = q.pop()
        if v not in seen:
            seen.add(v)
            q.extend(graph[v][0])

            while stack and v not in graph[stack[-1]][0]:
                order.append(stack.pop())
            stack.append(v)

    return stack + order[::-1]


graph = {
    1: [[2, 4],  # из 1 в 2 с весом 1 && из 1 в 4 с весом 1
        [1, 1]],
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

topologicaly_sorted = iterative_topological_sort(graph, start=1)
print(topologicaly_sorted)
print(graph)
