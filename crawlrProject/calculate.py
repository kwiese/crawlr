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
        
        for i in keyindices:
            keyword = keyindices[i]

            interest = 1
            weights[keyword] = int(interest)

            equality = data["{}-equality".format(i)]
            if equality != "NONE":
                try:
                    strict = int(data["{}-strictness".format(i)])
                except Exception as e:
                    edata = {"path": [], "addresses": [], "error": "Invalid equality value for {}!".format(keyword)}
                    return edata

                strictness[keyword] = (equality, strict)
            try:
                uHour = int(data["{}-hours".format(i)])*3600
            except Exception as e:
                uHour = 0
            try:
                uMinute = int(data["{}-minutes".format(i)])*60
            except Exception as e:
                uMinute = 0
            bounds[keyword] = (uHour + uMinute)
        
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
            if eq == "EQ" and not va == len(data["placeData"][k]):
                edata = {"path": [], "addresses": [], "error": "You said you wanted exactly {} {}'s, but we only found {}!".format(va, k, len(data["placeData"][k]))}
                return edata
            elif eq == "GTE" and va < len(data["placeData"][k]):
                edata = {"path": [], "addresses": [], "error": "You said you wanted at least {} {}'s, but we only found {}!".format(va, k, len(data["placeData"][k]))}
                return edata
            placenum += len(data["placeData"][k])
        if placenum == 0:
            edata = {"path": [], "addresses": [], "error": "We couldn't find any of the places you specified in your area!"}
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
