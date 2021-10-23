from graph import *

class QUBOMatrixFromGraph:
    matrix = list()
    row_size = 0
    path_length = 0
    vertexes = 0
    size = 0
    Lagrange = 10000
    graph = None
    graph_size = 0
    doubles = []
    finish = 0

    def __init__(self, graph_size, graph, start=0, finish=0, path_length=-1, points=[]):
        if path_length == -1:  # если не предсказали длинну пути - пусть будет как для гамильтонова цикла
            path_length = graph_size + 1

        self.doubles.append(finish)  # заводим фиктивную вершину финиша, после попадения в которую отдыхаем
        self.finish = graph_size

        self.doubles.extend(points)

        self.row_size = graph_size + len(self.doubles)

        self.path_length = path_length
        self.size = (path_length) * self.row_size
        self.matrix = [[0] * self.size for i in range(self.size)]
        self.graph = graph
        self.graph_size = graph_size

        self.fix_in_time(start, 0)
        self.fix_in_time(self.finish, self.path_length - 1)
        self.update_edges()
        for index in range(self.finish + 1, self.row_size):
            self.fix_one_in_place(index)
        for time in range(self.path_length):
            self.fix_one_in_time(time)

    def fix_one_in_place(self, index):  # Запрещает появляться в index != 1 раза
        for i in range(self.path_length):
            for j in range(self.path_length):
                if i == j:
                    self.matrix[i * self.row_size + index][i * self.row_size + index] -= 1 * self.Lagrange
                else:
                    self.matrix[i * self.row_size + index][j * self.row_size + index] += 2 * self.Lagrange

    def fix_one_in_time(self, time):  # Фиксирует ровно одну вершину пути для момента времени time
        for i in range(self.row_size):
            for j in range(self.row_size):
                if i == j:
                    self.matrix[time * self.row_size + i][time * self.row_size + i] -= 1 * self.Lagrange
                else:
                    self.matrix[time * self.row_size + i][time * self.row_size + j] += 2 * self.Lagrange

    def update_edges(self):  # Учитывает веса рёбер в матрице
        for time in range(self.path_length - 1):
            for i in range(self.row_size):
                for j in range(self.row_size):
                    self.update_edge(time, i, j)

    def update_edge(self, time, from_v, to_v):
        f = from_v
        t = to_v
        if t == self.finish and f == self.finish:
            return
        while from_v >= self.graph_size:  # если вершины - дубли а не из графа, достанем значения оригинала
            from_v = self.doubles[from_v - self.graph_size]
        while to_v >= self.graph_size:
            to_v = self.doubles[to_v - self.graph_size]
        edge = self.graph.edges[from_v][to_v]
        if f != t and from_v == to_v:
            return
        self.matrix[time * self.row_size + f][(time + 1) * self.row_size + t] += edge

    def fix_in_time(self, index, time):  # Фиксирует вершину Index на шаге time
        for i in range(self.row_size):
            if i != index:
                self.matrix[time * self.row_size + i][time * self.row_size + i] += 1 * self.Lagrange

    def get_matrix(self):
        return self.matrix

    def get_row_size(self):
        return self.row_size

    def get_path_size(self):
        return self.path_length

    def print_option(self, opt):
        i = 0
        c = 0
        for j in range(len(opt)):
            if opt[j] == 1:
                c += 1
                i = j
        if c != 1:
            print(opt)
            return
        if i < self.graph_size:
            print(i)
        if i == self.graph_size:
            print("f")
        if i > self.graph_size:
            print(str(self.doubles[i - self.graph_size]) + "'")


class QUBOMatrixFromGraphComm:
    matrix = list()
    row_size = 0
    path_length = 0
    vertexes = 0
    size = 0
    Lagrange = 10000
    graph = None
    graph_size = 0
    doubles = []
    finish = 0

    def __init__(self, graph_size, graph, start=0):
        self.doubles.append(start)  # заводим фиктивную вершину финиша, после попадения в которую отдыхаем
        self.finish = graph_size

        self.row_size = graph_size + len(self.doubles)

        self.path_length = graph_size + 1
        self.size = self.path_length * self.row_size
        self.matrix = [[0] * self.size for i in range(self.size)]
        self.graph = graph
        self.graph_size = graph_size

        self.fix_in_time(start, 0)
        self.fix_in_time(self.finish, self.path_length - 1)
        self.update_edges()
        for index in range(self.row_size):
            self.fix_one_in_place(index)
        for time in range(self.path_length):
            self.fix_one_in_time(time)

    def fix_one_in_place(self, index):  # Запрещает появляться в index != 1 раза
        for i in range(self.path_length):
            for j in range(self.path_length):
                if i == j:
                    self.matrix[i * self.row_size + index][i * self.row_size + index] -= 1 * self.Lagrange
                else:
                    self.matrix[i * self.row_size + index][j * self.row_size + index] += 2 * self.Lagrange

    def fix_one_in_time(self, time):  # Фиксирует ровно одну вершину пути для момента времени time
        for i in range(self.row_size):
            for j in range(self.row_size):
                if i == j:
                    self.matrix[time * self.row_size + i][time * self.row_size + i] -= 1 * self.Lagrange
                else:
                    self.matrix[time * self.row_size + i][time * self.row_size + j] += 2 * self.Lagrange

    def update_edges(self):  # Учитывает веса рёбер в матрице
        for time in range(self.path_length - 1):
            for i in range(self.row_size):
                for j in range(self.row_size):
                    self.update_edge(time, i, j)

    def update_edge(self, time, from_v, to_v):
        f = from_v
        t = to_v
        if t == self.finish and f == self.finish:
            return
        while from_v >= self.graph_size:  # если вершины - дубли а не из графа, достанем значения оригинала
            from_v = self.doubles[from_v - self.graph_size]
        while to_v >= self.graph_size:
            to_v = self.doubles[to_v - self.graph_size]
        edge = self.graph.edges[from_v][to_v]
        if f != t and from_v == to_v:
            return
        self.matrix[time * self.row_size + f][(time + 1) * self.row_size + t] += edge

    def fix_in_time(self, index, time):  # Фиксирует вершину Index на шаге time
        for i in range(self.row_size):
            if i != index:
                self.matrix[time * self.row_size + i][time * self.row_size + i] += 1 * self.Lagrange

    def get_matrix(self):
        return self.matrix

    def get_row_size(self):
        return self.row_size

    def get_path_size(self):
        return self.path_length

    def print_option(self, opt):
        i = 0
        c = 0
        for j in range(len(opt)):
            if opt[j] == 1:
                c += 1
                i = j
        if c != 1:
            return opt
        if i < self.graph_size:
            return i
        if i == self.graph_size:
            return "f"
