import numpy as np
from pyscr_QUBO import *
import json


def solve_text_case(s, start, end=-1):  # тесттаска, 5 станций, проехать по всем со стартовой по циклу или до какой-то
    if end == -1:
        end = start

    with open("test_stations.json", 'r', encoding='utf-8') as file:  # json с пятью станциями
        data = json.load(file)
    file.close()

    names = dict(zip([data['stations'][i]['name'] for i in range(len(data['stations']))],
                     [i for i in range(len(data['stations']))]))  # словарь имя->индекс

    n = len(names)  # предпостройка графа
    G = Graph(n)
    for i in range(n):
        for item in data['stations'][i]['able_to_get_to']:
            G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])

    QUBO_obj = QUBOMatrixFromGraphComm(n, G, start=names[start], end=names[end])  # генерим QUBO
    Q = QUBO_obj.get_matrix()  # достаём его из генератора

    spins, energy = s.solve_qubo(Q, timeout=1)  # пускаем на солвера Q, спины это наш Х, енергия может пригодиться

    np.save("test_logs/adjacency.npy", Graph.edges)  # логируем граф (для тесттаски)
    np.save("test_logs/Q.npy", Q)  # логируем Q (тож для тесттаски)
    np.save("test_logs/spins.npy", spins)  # Х тоже залогируем

    return QUBO_obj.format_x_to_ret(spins, data, names, start, G)
