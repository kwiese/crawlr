"""
Authors: Sean Donohoe

A flask server for interfacing the linear program with users
"""

import logging
import traceback

from flask import Flask, request, send_file, jsonify
from www.app import MyApp
from www.bounds import time_constraints
from data_collection.data_collection import collectData
from solver.value_solver_gurobi import solve

app = Flask(__name__)
mapp = None

@app.route("/")
def index():
    return app.send_static_file('index_home.html')

@app.route("/application")
def application():
    return app.send_static_file('index.html')

@app.route('/getRoute/', methods=['GET', 'POST'])
def solveRoute():
    if request.method == "POST":
        d = {}

        keywords = []
        for keyword in time_constraints:
            kname = "{}-selected".format(keyword)
            if kname in request.form:
                keywords.append(keyword)
        d["keywords"] = keywords
        
        d["start_address"] = request.form["start_address"]

        d["radius"] = int(request.form["searchRadius"])

        d["budget"] = int(request.form["budget"])

        hour = int(request.form["userHour"])
        minute = int(request.form["userMinute"])

        d["time"] = (hour + minute)

        weights = {"HOME": 0}
        strictness = {}
        bounds = {"HOME": 0}
        for keyword in keywords:
            kname = "{}-multiplier".format(keyword)
            weights[keyword] = int(request.form[kname])

            kname = "{}-equality".format(keyword)
            equality = request.form[kname]
            if equality != "NONE":
                kname = "{}-strictness".format(keyword)
                value = int(request.form[kname])

                strictness[keyword] = (equality, value)

            kname = "{}-upperHour".format(keyword)
            upperHour = int(request.form[kname])
            kname = "{}-upperMinute".format(keyword)
            upperMinute = int(request.form[kname])
            bounds[keyword] = (upperHour + upperMinute)

        d["weights"] = weights
        d["strictness"] = strictness
        d["bounds"] = bounds

        print(d)

        data = collectData(d)
        print("DONE COLLECTING DATA")
        try:
            path_data = solve(data)
        except:
            logging.error(traceback.format_exc())
            edata = {"path": [], "addresses": []}
            return jsonify(**edata)

        return jsonify(**path_data)
    else:
        return "ERROR"

if __name__ == '__main__':
    mapp = MyApp()
    app.run(host='0.0.0.0', port=8002)
