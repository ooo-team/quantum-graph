from qboard import Solver
import numpy as np
from QUBO import *
import json


def solve_case(start, finish, stations):
    PARAMS = {
        "remote_addr": "https://remote.qboard.tech",
        "access_key": "8a9c6702-ee8c-4cdc-a857-801f06cbd886"
    }

    s = Solver(mode="remote:simcim", params=PARAMS)

    with open("../test_stations.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    names = dict(zip([data['stations'][i]['name'] for i in range(len(data['stations']))],
                     [i for i in range(len(data['stations']))]))
    print(names)

    n = len(names)
    G = Graph(n)
    for i in range(n):
        for item in data['stations'][i]['able_to_get_to']:
            G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])
        if 'transfer' in data['stations'][i].keys():
            for item in data['stations'][i]['transfer']:
                G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])

    for i in range(n):
        print(G.edges[i])

    points = [names[name] for name in stations]

    QUBO_obj = QUBOMatrixFromGraph(n, G, start=names[start], finish=names[finish], points=points)
    Q = QUBO_obj.get_matrix()

    # Getting results
    spins, energy = s.solve_qubo(Q, timeout=1)

    for i in range(QUBO_obj.get_path_size()):
        QUBO_obj.print_option(spins[i * QUBO_obj.get_row_size():(i + 1) * QUBO_obj.get_row_size()])
