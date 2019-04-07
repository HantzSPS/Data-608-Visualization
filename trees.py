from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd


app = Flask(__name__)


# This is an API meant to serve some trees data in New York City
@app.route('/trees/<string:boroname>/<string:spc_common>')
def return_trees_data(boroname, spc_common):

    # Read in raw data
    raw_data = pd.read_json(
        'https://data.cityofnewyork.us/resource/nwxe-4ae8.json')
    

    # Filter based on borough and common species
    filtered_data = raw_data.loc[(raw_data['boroname'] == boroname) & (raw_data['spc_common'] == spc_common),
                                 ['boroname', 'spc_common', 'health']]

    
    # Build our json, then return it with jsonify
    filtered_data_json = {
        
        'Borough': filtered_data['boroname'].tolist(),
        'Species': filtered_data['spc_common'].tolist(),
        'Health': filtered_data['health'].tolist()
    }

    return jsonify(filtered_data_json)


# This routing allows us to view index.html
@app.route('/')
def index():
    return render_template('index.html')


# This routing allows us to load local Javascript
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(debug=True)
