from qboard import Solver
import numpy as np
from graph import *
from QUBO import *
import json

PARAMS = {
    "remote_addr": "https://remote.qboard.tech",
    "access_key": "8a9c6702-ee8c-4cdc-a857-801f06cbd886"
}

s = Solver(mode="remote:simcim", params=PARAMS)

'''
n = 5
G = Graph(n)
for i in range(n):
    G.add_edge(i, (i + 1) % n, 20)
    G.add_edge(i, (i + 2) % n, 10)
for i in range(n):
    print(G.edges[i])
'''

with open("test_stations.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

names = dict(zip([data['stations'][i]['name'] for i in range (len(data['stations']))], [i for i in range (len(data['stations']))]))
print(names)

n = len(names)
G = Graph(n)
for i in range(n):
    for item in data['stations'][i]['able_to_get_to']:
        G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])



for i in range(n):
    print(G.edges[i])

np.save("adjacency.npy", Graph.edges)

QUBO_obj = QUBOMatrixFromGraphComm(n, G, start=names['Арбатская'])
Q = QUBO_obj.get_matrix()

np.save("Q.npy", Q)

for i in range(len(Q)):
    print(Q[i])

# Getting results
spins, energy = s.solve_qubo(Q, timeout=1)

np.save("spins.npy", spins)

for i in range(QUBO_obj.get_path_size()):
    stant = QUBO_obj.print_option(spins[i*QUBO_obj.get_row_size():(i+1)*QUBO_obj.get_row_size()])
    if stant != 'f':
        print(data['stations'][stant]['name'])
    else:
        print('Арбатская')
