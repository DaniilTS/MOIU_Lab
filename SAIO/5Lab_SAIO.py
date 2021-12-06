import pprint


class Graph:

    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
        self.A = dict()
        self.M = 0
        self.V = dict()
        self.G = []

    def add_vector(self, x, y, c):
        if self.A.get(x) is None:
            self.A[x] = dict()
            self.V[x] = None
        if self.A.get(y) is None:
            self.V[y] = None
        self.A[x][y] = [0, c, 0]

    def check_back_vector(self):
        temp_v = []
        for x in self.A.keys():
            for y in self.A[x].keys():
                if self.A.get(y) is None or self.A[y].get(x) is None:
                    temp_v.append([y, x])
        for x, y in temp_v:
            self.add_vector(x, y, 0)
        pprint.pprint('Полная сеть:{}'.format(self.A))

    def calculate_M(self):
        self.M = 0
        for key in self.A[self.start].keys():
            self.M += self.A[self.start][key][0] - self.A[key][self.start][0]
        pprint.pprint('Мощность потока:{}'.format(self.M))

    def build_auxiliary_graph(self,way):
        if way is None:
            for x_key in self.A.keys():
                for y_key in self.A[x_key].keys():
                    self.A[x_key][y_key][2] = self.A[x_key][y_key][1] - self.A[x_key][y_key][0] + self.A[y_key][x_key][0]
        else:
            for index, node in enumerate(way):
                if index == len(way) - 1:
                    continue
                x_key = node
                y_key = way[index + 1]
                self.A[x_key][y_key][2] = self.A[x_key][y_key][1] - self.A[x_key][y_key][0] + self.A[y_key][x_key][0]
                x_key = way[index + 1]
                y_key = node
                self.A[x_key][y_key][2] = self.A[x_key][y_key][1] - self.A[x_key][y_key][0] + self.A[y_key][x_key][0]
        pprint.pprint('Вспомогательная сеть:{}'.format(self.A))

    def find_way(self):
        for key in self.V.keys():
            self.V[key] = None
        l = self.start
        self.V[l] = 0
        self.G.append(l)
        while len(self.G) != 0:
            l = self.G.pop(0)
            for y in self.A[l].keys():
                if self.A[l][y][2] != 0 and self.V[y] is None:
                    self.V[y] = l
                    self.G.append(y)

        pprint.pprint('Раставленные метки в вершины:{}'.format(self.V))
        if self.V[self.finish] is None:
            pprint.pprint('Максимальная мощность потока:{}'.format(self.M))
            return None

        way = [self.finish]
        while True:
            if self.V.get(way[-1]) is None:
                break
            way.append(self.V.get(way[-1]))
        way.pop()
        way.reverse()
        pprint.pprint('Путь:{}'.format(way))
        return way

    def add_steam(self, way):
        min_force = self.A[way[0]][way[1]][1]
        for index in range(1, len(way) - 1):
            if min_force > self.A[way[index]][way[index + 1]][1]:
                min_force = self.A[way[index]][way[index + 1]][1]
        pprint.pprint('Минимальная дуга из найденого пути:{}'.format(min_force))

        for x_key in self.A.keys():
            for y_key in self.A[x_key].keys():
                if x_key in way and y_key in way:
                    temp_f = 0
                    for index, node in enumerate(way):
                        if index == len(way) - 1:
                            continue
                        if x_key == node and way[index + 1] == y_key:
                            temp_f = min_force
                        elif y_key == node and way[index + 1] == x_key:
                            temp_f = min_force
                    self.A[x_key][y_key][0] = max(0, self.A[x_key][y_key][0] - self.A[y_key][x_key][0] + temp_f)
                else:
                    self.A[x_key][y_key][0] = max(0, self.A[x_key][y_key][0] - self.A[y_key][x_key][0])
        pprint.pprint('Новый граф:{}'.format(self.A))

    def run(self):
        way = None
        while True:
            self.calculate_M()
            self.build_auxiliary_graph(way)
            way = self.find_way()
            if way is None:
                break
            self.add_steam(way)


def ford_alg(graph):
    graph.check_back_vector()
    graph.run()


if __name__ == '__main__':
    # graph = Graph(1, 4)
    # graph.add_vector(1, 2, 3)
    # graph.add_vector(1, 3, 2)
    # graph.add_vector(2, 3, 2)
    # graph.add_vector(2, 4, 1)
    # graph.add_vector(3, 4, 2)
    graph = Graph(1, 6)
    graph.add_vector(1, 2, 7)
    graph.add_vector(1, 3, 4)
    graph.add_vector(2, 3, 4)
    graph.add_vector(2, 4, 2)
    graph.add_vector(3, 4, 8)
    graph.add_vector(3, 5, 4)
    graph.add_vector(4, 5, 4)
    graph.add_vector(4, 6, 5)
    graph.add_vector(5, 6, 12)
    ford_alg(graph)
