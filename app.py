from flask import Flask, render_template, request

app = Flask(__name__)

stations = [{'name': 'option1'},  {'name': 'option2'},  {'name': 'option3'},  {'name': 'option4'}
          , {'name': 'option5'},  {'name': 'option6'},  {'name': 'option7'},  {'name': 'option8'}
          , {'name': 'option9'},  {'name': 'option10'}, {'name': 'option11'}, {'name': 'option12'}
          , {'name': 'option13'}, {'name': 'option14'}, {'name': 'option15'}, {'name': 'option16'}
          , {'name': 'option17'}, {'name': 'option18'}, {'name': 'option19'}, {'name': 'option20'}
          , {'name': 'option21'}, {'name': 'option22'}, {'name': 'option23'}, {'name': 'option24'}]

@app.route('/')
def autocomplete():
    return render_template("input_dropdown.html", data=stations)


@app.route('/', methods=['POST'])
def autocomplete_post():
    text = request.form['station']
    processed_text = text
    print(processed_text)
    return render_template('input_dropdown.html', data=stations), 201


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/map')
def maps():
    return render_template('mapbasics.html')
