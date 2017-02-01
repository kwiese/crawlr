"""
Authors: Sean Donohoe

A flask server for interfacing the linear program with users
"""

from flask import Flask, request, send_file, jsonify, json
from data_collection import collectData
import traceback
from log import log

app = Flask(__name__)

@app.route("/query", methods=['GET', 'POST'])
def query():
    log(request.json)
    if request.method == "POST":
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
        j = None
        try:
            safe = json.loads(json.htmlsafe_dumps(ret))
            j = jsonify(**safe)
        except Exception as e:
            log(traceback.format_exc())
            wut = {"fail": "fail"}
            return jsonify(**wut)
        return jsonify(**ret)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
