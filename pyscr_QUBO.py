from pyscr_graph import *


class QUBOMatrixFromGraphComm:  # QUBO генератор для графа (гамильтонов путь или цикл)
    matrix = list()  # QUBO
    row_size = 0  # сколько батч содержит координат (общее число вершин включая фиктивные)
    path_length = 0  # сколько батчей содержит вектор Х который минимизируем
    size = 0  # размер вектора Х который минимизируем
    Lagrange = 10000  # коофицент лагранжа (должен быть знач. больше суммы весов пути)
    graph = Graph(0)  # коофицент лагранжа (должен быть знач. больше суммы весов пути)
    doubles = []  # индексы фиктивных вершин (у нас гамильтонова задача, тут либо [], либо цикл, тогда храним finish)
    finish = 0  # finish показывает где путь закончится, храним чтоб обрабатывать финальные шаги правильно

    def __init__(self, graph_size, graph, start=0, end=-1):  # Граф и старт затребуем, остальное примем за [] или same

        if end == -1:  # если не дали конца - построим цикл
            end = start
        self.doubles = []  # инициализируем фиктивные вершины
        if start == end:
            self.doubles.append(start)  # заводим фиктивную вершину финиша если у нас цикл
            self.finish = graph_size  # без неё в finish==start попасть в конце не выйдет
        else:
            self.finish = end  # если не цикл всё ок, финишируем просто в последней

        self.row_size = graph_size + len(self.doubles)  # в батче будут 1/0 на все вершины, 1 если на i-том шаге в ней

        self.path_length = self.row_size  # путь идёт по всем верщинам (в том числе фиктивным)

        self.size = self.path_length * self.row_size  # инициализируем QUBO нужного размера
        self.matrix = [[0] * self.size for i in range(self.size)]

        self.graph_size = graph_size

        self.fix_in_time(start, 0)  # первая вершина всегда старт
        self.fix_in_time(self.finish, self.path_length - 1)  # последняя вершина всегда финиш
        self.update_edges(graph)  # прикручиваем веса рёбер графа
        for index in range(self.row_size):  # запрещаем брать вершину в путь дважды
            self.fix_one_in_place(index)
        for time in range(self.path_length):  # запрещаем брать две вершины на одном и том же шагу
            self.fix_one_in_time(time)

    def fix_one_in_place(self, index):  # по сути ставим кандишн на минимизацию (x1 + y1 + ... + z1 - 1)^2
        for i in range(self.path_length):
            for j in range(self.path_length):
                if i == j:
                    self.matrix[i * self.row_size + index][i * self.row_size + index] -= 1 * self.Lagrange
                else:
                    self.matrix[i * self.row_size + index][j * self.row_size + index] += 2 * self.Lagrange

    def fix_one_in_time(self, time):  # так же ставим кандишн на минимизацию (x1 + x2 + ... + xn - 1)^2
        for i in range(self.row_size):
            for j in range(self.row_size):
                if i == j:
                    self.matrix[time * self.row_size + i][time * self.row_size + i] -= 1 * self.Lagrange
                else:
                    self.matrix[time * self.row_size + i][time * self.row_size + j] += 2 * self.Lagrange

    def update_edges(self, graph):  # пробегаем все рёбра во все моменты времени
        for time in range(self.path_length - 1):
            for i in range(self.row_size):
                for j in range(self.row_size):
                    self.update_edge(time, i, j, graph)

    def update_edge(self, time, from_v, to_v, graph):  # накидываем вес на них
        f = from_v
        t = to_v
        while from_v >= self.graph_size:  # если from - фиктивная, достанем индекс оригинала
            from_v = self.doubles[from_v - self.graph_size]
        while to_v >= self.graph_size:  # аналогично для to
            to_v = self.doubles[to_v - self.graph_size]
        edge = graph.edges[from_v][to_v]  # длинна ребра оригиналов
        if f != t and from_v == to_v:  # как это водится, из себя в копию можно попасть за 0 (у копий всегда гам. усл.)
            return
        self.matrix[time * self.row_size + f][(time + 1) * self.row_size + t] += edge  # накидываем вес куда надо

    def fix_in_time(self, index, time):  # фиксирует вершину Index на шаге time
        for i in range(self.row_size):
            if i != index:  # запрещаем просто - если взяли не ту - кидаем здоровый штраф
                self.matrix[time * self.row_size + i][time * self.row_size + i] += 1 * self.Lagrange

    def get_matrix(self):  # геттеры на всякий случай чтобы никто не дай бог сюда не залез
        return self.matrix

    def get_row_size(self):
        return self.row_size

    def get_path_size(self):
        return self.path_length

    def print_option(self, opt):  # интерпритатор батча, вернёт индекс или f если в фиктивной вершинке
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

    def format_x_to_ret(self, spins, data, names, start, graph):
        # формируем вывод, нужны названия станций подряд и время между ними

        out = []  # названия
        vertexes = []  # индексы (для расчёта времени через граф)
        times = []  # интервалы времени

        for i in range(self.get_path_size()):  # для отработки по-батчам надо пользоваться тем какой размер Q
            # трансляция батча в индекс через метод QUBO объекта, чтобы формат учесть, довольно кринжово, oh well
            batch = self.print_option(spins[i * self.get_row_size():(i + 1) * self.get_row_size()])
            if batch != 'f':  # Кидаем имя станции и индекс в листы
                vertexes.append(batch)
                out.append(data['stations'][batch]['name'])
            else:
                vertexes.append(names[start])
                out.append(start)

        for i in range(len(vertexes) - 1):  # Проходимся по рёбрам, пишем интервалы в листы
            times.append(graph.edges[vertexes[i]][vertexes[i + 1]])
        return out, times
