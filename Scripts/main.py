from qboard import Solver
import numpy as np
from graph import *
from QUBO import *

PARAMS = {
    "remote_addr": "https://remote.qboard.tech",
    "access_key": "8a9c6702-ee8c-4cdc-a857-801f06cbd886"
}
s = Solver(mode="remote:simcim", params=PARAMS)

n = 4
G = Graph(n)
for i in range(n - 1):
    G.add_edge(i, (i + 1) % n, 20)
G.add_edge(0, 2, 20)
G.add_edge(1, 3, 20)
G.add_edge(0, 3, 5)
G.add_edge(2, 3, 2)
for i in range(n):
    print(G.edges[i])

QUBO_obj = QUBOMatrixFromGraph(n, G, path_length=10, finish=2, points=[1, 2])
Q = QUBO_obj.get_matrix()

for i in range(len(Q)):
    print(Q[i])

# Getting results
spins, energy = s.solve_qubo(Q, timeout=1)

for i in range(QUBO_obj.get_path_size()):
    QUBO_obj.print_option(spins[i*QUBO_obj.get_row_size():(i+1)*QUBO_obj.get_row_size()])
