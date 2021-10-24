from qboard import Solver
import numpy as np
from QUBO import *
import json


def create_solver_connection():
    PARAMS = {
        "remote_addr": "https://remote.qboard.tech",
        "access_key": "8a9c6702-ee8c-4cdc-a857-801f06cbd886"
    }
    s = Solver(mode="remote:simcim", params=PARAMS)
    return s


def solve_text_case(start, s):
    with open("./test_stations.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    names = dict(zip([data['stations'][i]['name'] for i in range(len(data['stations']))],
                     [i for i in range(len(data['stations']))]))
    print(names)

    n = len(names)
    G = Graph(n)
    for i in range(n):
        for item in data['stations'][i]['able_to_get_to']:
            G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])

    #for i in range(n):
    #    print(G.edges[i])

    np.save("adjacency.npy", Graph.edges)

    QUBO_obj = QUBOMatrixFromGraphComm(n, G, start=names[start])
    Q = QUBO_obj.get_matrix()
    file.close()
    np.save("Q.npy", Q)
    print(len(Q), "len Q")
    # Getting results
    spins, energy = s.solve_qubo(Q, timeout=1)

    np.save("spins.npy", spins)

    out = list()
    vertexes = []
    times = []

    for i in range(QUBO_obj.get_path_size()):
        stant = QUBO_obj.print_option(spins[i * QUBO_obj.get_row_size():(i + 1) * QUBO_obj.get_row_size()])
        if stant != 'f':
            vertexes.append(stant)
            out.append(data['stations'][stant]['name'])
        else:
            vertexes.append(names[start])
            out.append(start)
    final_time = 0

    for i in range(len(vertexes) - 1):
        times.append(G.edges[vertexes[i]][vertexes[i + 1]])
        final_time += G.edges[vertexes[i]][vertexes[i + 1]]
    print(final_time, "время на путь")

    import csv
    file = open('answer.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows([out])

    return out, times
