import json

with open('../stations.json', 'r') as st_file:
    data = json.load(st_file)

stations = data['stations']

def find_station(name):
    for station in enumerate(stations):
        if station[1]['name'] == name:
            return station[0]
    pass

for station in stations:
    for to_station in station['able_to_get_to']:
        if find_station(to_station['to']) == None:
            print('somethong bad happaned on', station['name'], 'with', to_station['to'])
            continue
        if stations[find_station(to_station['to'])]['name'] != to_station['to']:
            print('no backwards connection between', station['name'], to_station['to'])