import numpy as np
from pyscr_QUBO import *
import json


def solve_case(s, start, end=-1, points=[]):  # финалка, внутриенность колца, от start до end + все из points
    if end == -1:
        end = start

    with open("stations.json", 'r', encoding='utf-8') as file:  # json со всеми станциями внутри кольца
        data = json.load(file)
    file.close()

    names = dict(zip([data['stations'][i]['name'] for i in range(len(data['stations']))],
                     [i for i in range(len(data['stations']))]))  # словарь имя->индекс

    n = len(names)  # предпостройка графа, важно что тут у станции может быть transfer и его важно обработать
    G = Graph(n)
    for i in range(n):
        for item in data['stations'][i]['able_to_get_to']:
            G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])
        if 'transfer' in data['stations'][i].keys():  # вот тут не забываем их докинуть
            for item in data['stations'][i]['transfer']:
                G.add_edge(names[data['stations'][i]['name']], names[item['to']], item['time'])

    # стянем граф до вершин которые надо посетить, начала и конца, для начала сохраним их все в points
    if start not in points:
        points.append(start)
    if end not in points:
        points.append(end)

    G = G.shrink([names[name] for name in points])  # стягиваем

    names = dict()  # надо обновить индексы, теперь
    for i in range(len(points)):
        names[points[i]] = i

    QUBO_obj = QUBOMatrixFromGraphComm(len(points), G, start=names[start], end=names[end])  # генерим QUBO
    Q = QUBO_obj.get_matrix()  # достаём его из генератора

    spins, energy = s.solve_qubo(Q, timeout=1)  # пускаем на солвера Q, спины это наш Х, енергия может пригодиться
    ways = QUBO_obj.format_x_to_ret(spins, data, names, start, G)
    import csv
    file = open('test_logs/answer.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows([ways[0]])
    return ways  # форматируем X по размеру QUBO_obj
