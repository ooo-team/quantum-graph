from flask import Flask, render_template, request
import json
import test_task

app = Flask(__name__)

with open('test_stations.json', 'r', encoding='utf-8') as metro_graph:
    stations = json.load(metro_graph)['stations']

@app.route('/')
def autocomplete():
    return render_template("input_dropdown.html", data=stations)


@app.route('/', methods=['POST'])
def autocomplete_post():
    text = request.form['station']
    processed_text = test_task.solve_text_case(text)
    print(processed_text)
    return render_template('input_dropdown.html', data=stations, processed_text=processed_text), 201


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/map')
def maps():
    return render_template('mapbasics.html')
