class Graph:
    INF = 10000
    size = 0
    edges = list()

    def __init__(self, size):
        self.size = size
        self.edges = [[self.INF] * size for i in range(size)]

    def add_edge(self, index1, index2, time):
        print(index1, index2)
        if self.edges[index1][index2] > time:
            self.edges[index1][index2] = time
            self.edges[index2][index1] = time

    def add_edges(self, edges):
        self.edges = edges


