from bounds import time_constraints
from data_collection.data_collection import collectData
from solver.value_solver import solve
import traceback

from log import log


def start_chain(data):
    log("starting chain")
    try:
        keywords = []
        d = {}
        for keyword in time_constraints:
            kname = "{}-selected".format(keyword)
            if kname in data:
                keywords.append(keyword)
        d["keywords"] = keywords

        d["start_address"] = data["start_address"]

        d["radius"] = int(data["searchRadius"])

        d["budget"] = int(data["budget"])

        hour = int(data["userHour"])
        minute = int(data["userMinute"])

        d["time"] = (hour + minute)

        weights = {"HOME": 0}
        strictness = {}
        bounds = {"HOME": 0}
        for keyword in keywords:
            kname = "{}-multiplier".format(keyword)
            weights[keyword] = int(data[kname])

            kname = "{}-equality".format(keyword)
            equality = data[kname]
            if equality != "NONE":
                kname = "{}-strictness".format(keyword)
                value = int(data[kname])

                strictness[keyword] = (equality, value)

            kname = "{}-upperHour".format(keyword)
            upperHour = int(data[kname])
            kname = "{}-upperMinute".format(keyword)
            upperMinute = int(data[kname])
            bounds[keyword] = (upperHour + upperMinute)

        d["weights"] = weights
        d["strictness"] = strictness
        d["bounds"] = bounds
        d["timestamp"] = " ".join(data["timestamp"].split("(")[:-1]).strip()

        data = collectData(d)
    except Exception as e:
        log(traceback.format_exc())
        edata = {"path": [], "addresses": []}
        return edata
    try:
        log("starting solving")
        path_data = solve(data)
    except:
        log(traceback.format_exc())
        edata = {"path": [], "addresses": []}
        return edata
    
    return path_data
