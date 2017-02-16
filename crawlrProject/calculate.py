from bounds import time_constraints
from data_collection.data_collection import collectData
from solver.value_solver import solve
import traceback
import time
import re

from log import log


def start_chain(data):
    log("starting chain")
    try:
        keywords = []
        keyindices = {}
        d = {}
        for element in data:
            m = re.match(
                r'k-([0-9]+)',
                element,
                re.M|re.I,
            )
            if m:
                val = data[element]
                mm = re.match(
                    r'(.+)-([0-9]+)',
                    val,
                    re.M|re.I,
                )
                k = mm.group(1)
                i = mm.group(2)
                keyindices[i] = k
                keywords.append(k)

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
        
        for i in keyindices:
            keyword = keyindices[i]

            interest = data["{}-interest".format(i)]
            weights[keyword] = int(interest)

            equality = data["{}-equality".format(i)]
            if equality != "NONE":
                strict = int(data["{}-strictness".format(i)])
                strictness[keyword] = (equality, strict)

            uHour = int(data["{}-hours".format(i)])*3600
            uMinute = int(data["{}-minutes".format(i)])*60
            bounds[keyword] = (uHour + uMinute)
        
        d["weights"] = weights
        d["strictness"] = strictness
        d["bounds"] = bounds
        d["timestamp"] = " ".join(data["timestamp"].split("(")[:-1]).strip()
        log(d)
        t = time.time()
        data = collectData(d)
        log("total data collection {}".format((time.time() - t)))
    except Exception as e:
        log(traceback.format_exc())
        edata = {"path": [], "addresses": []}
        return edata
    try:
        log("starting solving")
        t = time.time()
        path_data = solve(data)
        log("total solving {}".format((time.time() - t)))
    except:
        log(traceback.format_exc())
        edata = {"path": [], "addresses": []}
        return edata
    
    return path_data
