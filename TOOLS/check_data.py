import json
from os import stat

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
            print('somethong bad happaned on',
                  station['name'], 'with', to_station['to'])
            continue

for station in stations:
    if 'transfer' in station:
        for to_station in station['transfer']:
            if find_station(to_station['to']) == None:
                print('somethong bad happaned on transfer on',
                      station['name'], 'with', to_station['to'])
                continue


for station in stations:
    for to_station in station['able_to_get_to']:
        for deep_station in stations[find_station(to_station['to'])]['able_to_get_to']:
            if deep_station['to'] == station['name']:
                if deep_station['time'] != to_station['time']:
                    print(
                        f'not equal travel times on {to_station["to"]} and {deep_station["to"]} ({deep_station["time"]} != {to_station["time"]})')

for station in stations:
    if 'transfer' in station:
        for to_station in station['transfer']:
            if 'transfer' in stations[find_station(to_station['to'])]:
                for deep_station in stations[find_station(to_station['to'])]['transfer']:
                    if deep_station['to'] == station['name']:
                        if deep_station['time'] != to_station['time']:
                            print(
                                f'not equal travel times on {to_station["to"]} and {deep_station["to"]} ({deep_station["time"]} != {to_station["time"]})')

print(len(stations))
