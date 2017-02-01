"""
Authors: Sean Donohoe

A flask server for interfacing the linear program with users
"""

from flask import Flask, request
from log import log, plog

app = Flask(__name__)

@app.route("/event", methods=['POST'])
def event():
    data = request.get_json(silent=True)
    if not data:
        return "dummy"
    log(data["payload"])
    return "dummy"

@app.route("/perf", methods=['POST'])
def perf():
    data = request.get_json(silent=True)
    if not data:
        return "dummy"
    plog(data["payload"])
    return "dummy"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
