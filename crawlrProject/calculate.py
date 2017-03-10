from bounds import time_constraints
from data_collection.data_collection import collectData
from solver.value_solver import solve
import traceback
import time

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
        if not len(keywords):
            edata = {"path": [], "addresses": [], "error": "You didn't specify the kinds of places you want to visit!"}
            return edata

        d["start_address"] = data["start_address"]
        if not len(data["start_address"].strip()):
            edata = {"path": [], "addresses": [], "error": "You didn't specify a start address!"}
            return edata

        try:
            d["radius"] = int(data["searchRadius"])
            if (d["radius"] is not 805) or (d["radius"] is not 1609) or (d["radius"] is not 2414):
                edata = {"path": [], "addresses": [], "error": "The search radius is an invalid value!"}
                return edata
        except Exception as e:
            edata = {"path": [], "addresses": [], "error": "The search radius is an invalid value!"}
            return edata

        try:
            d["budget"] = int(data["budget"])
            if d["budget"] < 0 or d["budget"] > 4:
                edata = {"path": [], "addresses": [], "error": "The budget is an invalid value!"}
                return edata
        except Exception as e:
            edata = {"path": [], "addresses": [], "error": "The budget is an invalid value!"}
            return edata

        try:
            hour = int(data["userHour"])
        except Exception as e:
            edata = {"path": [], "addresses": [], "error": "Invalid value for your hours available!"}
            return edata
        try:
            minute = int(data["userMinute"])
        except Exception as e:
            edata = {"path": [], "addresses": [], "error": "Invalid value for your minutes available!"}
            return edata

        d["time"] = (hour + minute)

        weights = {"HOME": 0}
        strictness = {}
        bounds = {"HOME": 0}
        for keyword in keywords:
            weights[keyword] = 1

            kname = "{}-equality".format(keyword)
            equality = data[kname]
            if equality != "NONE":
                kname = "{}-strictness".format(keyword)
                try:
                    value = int(data[kname])
                except Exception as e:
                    edata = {"path": [], "addresses": [], "error": "Invalid equality value for {}!".format(keyword)}
                    return edata

                strictness[keyword] = (equality, value)

            kname = "{}-upperHour".format(keyword)
            try:
                upperHour = int(data[kname])
            except Exception as e:
                upperHour = 0
            kname = "{}-upperMinute".format(keyword)
            try:
                upperMinute = int(data[kname])
            except Exception as e:
                upperMinute = 0
            bounds[keyword] = (upperHour + upperMinute)

        d["weights"] = weights
        d["strictness"] = strictness
        d["bounds"] = bounds
        d["timestamp"] = " ".join(data["timestamp"].split("(")[:-1]).strip()
        log(d)
        t = time.time()
        data = collectData(d)
        if "error" in data:
            edata = {"path": [], "addresses": [], "error": data["error"]}
            return edata
        placenum = 0
        for k in strictness:
            eq, va = strictness[k]
            if eq == "EQ" and va is not len(data["placeData"][k]):
                edata = {"path": [], "addresses": [], "error": "You said you wanted exactly {} {}'s, and we only found {}".format(va, k, len(data["placeData"][k])}
                return edata
            elif eq == "GTE" and va < len(data["placeData"][k]):
                edata = {"path": [], "addresses": [], "error": "You said you wanted at least {} {}'s, and we only found {}".format(va, k, len(data["placeData"][k])}
                return edata
            placenum += len(data["placeData"][k])
        if placenum == 0:
            edata = {"path": [], "addresses": [], "error": "We couldn't find any of the places you specified!"}
            return edata
        log("total data collection {}".format((time.time() - t)))
    except Exception as e:
        log(traceback.format_exc())
        edata = {"path": [], "addresses": [], "error": "Something went wrong when we tried getting your data!"}
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
