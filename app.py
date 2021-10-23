from flask import Flask, render_template, request
import json
import test_task

app = Flask(__name__)

with open('test_stations.json', 'r', encoding='utf-8') as metro_graph:
    stations = json.load(metro_graph)['stations']

slver = test_task.create_solver_connection()


@app.route('/')
def maps():
    return render_template("mapbasics.html", data=stations)


@app.route('/', methods=['POST'])
def maps_post():
    text = request.form['station']
    appropriate_stations = [i["name"] for i in stations]
    if text not in appropriate_stations:
        return render_template("mapbasics.html", data=stations), 400
    processed = test_task.solve_text_case(text, slver)
    total_time = sum(processed[1])
    processed[1].append(None)
    processed_text_time = list(zip(processed[0], processed[1]))
    # print(list(processed_text_time))
    return render_template('mapbasics.html', data=stations, processed_text_time=processed_text_time, total_time=total_time), 201


if __name__ == '__main__':
    app.run(debug=True)


