from www.bounds import time_constraints
#from data_collection.data_collection import collectData
from solver.value_solver import solve

def start_chain(data):
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
        equality = request.form[kname]
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

    print(d)
    #
    # data = collectData(d)
    # print("DONE COLLECTING DATA")
    # try:
    #     path_data = solve(data)
    # except:
    #     edata = {"path": [], "addresses": []}
    #     return jsonify(**edata)
    #
    # return jsonify(**path_data)
