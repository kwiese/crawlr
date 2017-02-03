"""
Authors: Sean Donohoe

A flask server for interfacing the linear program with users
"""

from flask import Flask, request, Response, jsonify
import json
from data_collection import collectData
import traceback
from log import log

app = Flask(__name__)

@app.route("/query", methods=['POST'])
def query():
    data = request.get_json(silent=True)
    if not data:
        wut = {"fail": "fail"}
        return jsonify(**wut)
    try:
        ret = collectData(data)
    except Exception as e:
        log(traceback.format_exc())
    new_d = {}
    for k in ret["distance_data"]:
        frm, to = k
        new_k = frm + "__" + to
        new_d[new_k] = ret["distance_data"][k]
    ret["distance_data"] = new_d
    res = jsonify(user_data=ret["user_data"], place_data=ret["place_data"], distance_data=ret["distance_data"])
    res.status_code = 200
    return res



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
