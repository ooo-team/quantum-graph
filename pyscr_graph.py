class Graph:
    INF = 1000  # усли лагранж фиксирует требования на путь, инф сделан чтобы несуществ. рёбра имели хоть какой-то вес
    size = 0
    edges = list()  # матрица смежности

    def __init__(self, size):  # инициализация не очень умная
        self.size = size
        self.edges = [[self.INF] * size for i in range(size)]

    def add_edge(self, index1, index2, time):  # как кидаем рёбра
        if self.edges[index1][index2] > time:
            self.edges[index1][index2] = time
            self.edges[index2][index1] = time

    def add_edges(self, edges):  # кидаем всю матрицу если очень хотим (надо кидать корректную)
        self.edges = edges

    def shrink(self, vertexes):  # стягиваем граф до набора vertexes
        # так как между ними рёбер может не быть, найдём все расстояния (здесь бахнем Флойда, можно попарно Дейкстры)
        # в нашем случае буста выбор алгоритма особо не даст, так как считаться даже для всех станций в прицнипе
        # будет в разы быстрее чем обращаться к компу, но в целом для нашего примера с метро (степерь не больше 2+2)
        # 2 проезда и 2 перехода максимум, если реализовать Дейкстру за О(nlogn+mlogn) и m<=4n получим О(nlogn)
        # вывод - тут надо смотреть на масштаб и тип задачи, но в нашем случае и флоид за O(n^3) более чем достаточно
        dist = [self.edges[i].copy() for i in range(self.size)]

        for i in range(self.size):  # реализация Флоида
            for u in range(self.size):
                for v in range(self.size):
                    dist[u][v] = min(dist[u][v], dist[u][i] + dist[i][v])
        for i in range(self.size):  # Запретим петли (полезно для оптимизации работы на QUBO)
            dist[i][i] = self.INF

        # создадим граф только на vertexes, скопируем все расстояния туда, получится полный граф
        # мало того, что тогда на нём найдётся хотя-бы один гамильтонов цикл, любой мин путь из нашего изначального
        # графа будет иметь представление здесь (т.к. v[x,y]+v[y,z]>=v[x,z] по построению)
        new_graph = Graph(len(vertexes)) 
        for i in range(len(vertexes)):
            for j in range(len(vertexes)):
                new_graph.add_edge(i, j, dist[vertexes[i]][vertexes[j]])
        return new_graph
