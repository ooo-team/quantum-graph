class Graph:
    INF = 1000
    size = 0
    edges = list()

    def __init__(self, size):
        self.size = size
        self.edges = [[self.INF] * size for i in range(size)]

    def add_edge(self, index1, index2, time):
        if self.edges[index1][index2] > time:
            self.edges[index1][index2] = time
            self.edges[index2][index1] = time

    def add_edges(self, edges):
        self.edges = edges

    def shrink(self, vertexes):
        print(vertexes)
        dist = [self.edges[i].copy() for i in range(self.size)]
        for i in range(self.size):
            for u in range(self.size):
                for v in range(self.size):
                    dist[u][v] = min(dist[u][v], dist[u][i] + dist[i][v])
        for i in range(self.size):
            dist[i][i] = self.INF
        print(dist)

        new_graph = Graph(len(vertexes))
        for i in range(len(vertexes)):
            for j in range(len(vertexes)):
                new_graph.add_edge(i, j, dist[vertexes[i]][vertexes[j]])
        return new_graph
