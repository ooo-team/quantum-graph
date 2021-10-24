from flask import Flask, render_template, request
import json
import pyscr_solver_logic
import pyscr_custom_task

app = Flask(__name__)

with open('stations.json', 'r', encoding='utf-8') as metro_graph:
    stations = json.load(metro_graph)['stations']


appropriate_stations = [i["name"] for i in stations]
chosen_stations = []
slver = pyscr_solver_logic.create_solver_connection()


@app.route('/')
def maps():
    return render_template("mapbasics.html", data=stations)


@app.route('/', methods=['POST'])
def maps_post():
    if request.form["btn"]=="submit_stations":
        text = request.form['station']
        if text not in appropriate_stations:
            return render_template("mapbasics.html", data=stations, msg="Некорректный выбор!"), 400
        chosen_stations.append(request.form['station'])
        start = chosen_stations[0]
        finish = chosen_stations[-1]
        chosen_stations_unique = list(set(chosen_stations))
        chosen_stations.clear()
        processed = pyscr_custom_task.solve_case(slver, start, finish, chosen_stations_unique)
        chosen_stations_unique.clear()
        total_time = sum(processed[1])
        processed[1].append(None)
        processed_text_time = list(zip(processed[0], processed[1]))
        # print(list(processed_text_time))
        return render_template('mapbasics.html', data=stations, processed_text_time=processed_text_time, total_time=total_time), 201
    
    if request.form["btn"]=="add_station":
        text = request.form['station']
        if text not in appropriate_stations:
            return render_template("mapbasics.html", data=stations, msg="Некорректный выбор!"), 400
        chosen_stations.append(request.form['station'])
        return render_template("mapbasics.html", data=stations, msg="UwU Введите ещё..... Вы ввели "+ str(chosen_stations))

        


if __name__ == '__main__':
    app.run(debug=True)


