"""
Authors: Sean Donohoe and Kyle Wiese

An implementation for composing and solving the linear program, using the PuLP API
"""


from pulp import *
from www.bounds import time_constraints

var_mapping = {}

def cascade(data):
    timeArray = []
    decisionArray = []
    edgeArray = []
    keywordArray = []

    lp = LpProblem("value optimizer", LpMaximize)
    
    initialize(data, timeArray, decisionArray, edgeArray, keywordArray)

    addBudgetConstraint(data, decisionArray, lp)   
   
    addPathConstraint(data, decisionArray, edgeArray, lp)

    addTimeConstraint(data, timeArray, edgeArray, lp)

    addHomeConstraints(data, timeArray, decisionArray, lp)

    addDecisionConstraints(data, timeArray, decisionArray, lp) 

    addKeywordConstraints(data, decisionArray, keywordArray, lp)

    addObjectiveFunction(data, timeArray, decisionArray, edgeArray, lp)

    return (timeArray, decisionArray, edgeArray, keywordArray, lp)

def solve(data):
    
    (timeArray, decisionArray, edgeArray, keywordArray, lp) = cascade(data) 
    
    status = lp.solve(GLPK(msg=0))

    
    subtours = collectSubtours(edgeArray)
    while len(subtours) > 1:
        print(len(subtours))
        for subtour in subtours:
            addSubtourConstraint(data, subtour, edgeArray, lp)
        status = lp.solve(GLPK(msg=0))
        subtours = collectSubtours(edgeArray)

    print(LpStatus[status]) 
    chosenEdges = []
    
    for (e, t) in edgeArray:
        if value(e):
            frm = var_mapping[e.name].split(",")[0].strip()
            to = var_mapping[e.name].split(",")[1].strip()
            chosenEdges.append((frm, to))

    last = ""
    for x in chosenEdges:
        if x[0] == "HOME":
            last = x[1]
            chosenEdges.remove(x)
            break

    final_path = []
    final_addresses = []
    if len(chosenEdges) > 0:
        print("HOME")
        final_path.append("Home ({})".format(data["user_data"]["start_address"]))
        final_addresses.append(data["user_data"]["start_address"])
        while last != "HOME":
            last_t = None
            key = None
            for (y, k, p) in timeArray:
                if var_mapping[y.name] == last:
                    last_t = y
                    key = k
                    break
            last_d = None
            for (y, k, p) in decisionArray:
                if var_mapping[y.name] == last:
                    last_d = y
                    break
            print("{}: time: {}, place decision: {}".format(last, value(last_t), value(last_d)))
            pla = None
            for place in data["place_data"][key]:
                if place["name"] == last:
                    pla = place
                    break
            time_s = value(last_t)
            time_h = int(time_s) // 3600
            time_m = (int(time_s) - (time_h * 3600)) // 60
            tstring = None
            if time_h:
                if time_m:
                    tstring = "{} hours, {} minutes".format(time_h, time_m)
                else:
                    tstring = "{} hours".format(time_h)
            else:
                tstring = "{} minutes".format(time_m)

            rating = pla["original_rating"]
            budget = "$" * (pla["price_level"])
            website = pla["website"]
            last_s = last
            if website:
                last_s = "<a href={}>{}</a>".format(website, last_s)
            pitem = "{} ({}), Rating: {}, Price: {}, Spend {} here".format(last_s, key, rating, budget, tstring)
            final_path.append(pitem)
            final_addresses.append(pla["address"])
            for x in chosenEdges:
                if x[0] == last:
                    last = x[1]
                    chosenEdges.remove(x)
                    break

        print("HOME")
        final_path.append("Home ({})".format(data["user_data"]["start_address"]))
        final_addresses.append(data["user_data"]["start_address"])
    print(chosenEdges)
    print(final_addresses)
            
    print("Total: {}".format(value(lp.objective)))
    rdata = {
        "path": final_path,
        "addresses": final_addresses,
    }
    return rdata

def initialize(data, timeArray, decisionArray, edgeArray, keywordArray):
    # function to initialize the columns and rows of the problem
    global var_mapping
    curr_int = 0
    place_data = data["place_data"]
    user_data = data["user_data"]
    for keyword in user_data["strictness"]:
        (equality, value) = user_data["strictness"][keyword]
        kEntry = (keyword, equality, value)
        keywordArray.append(kEntry)

    gdata = [ place_data[k]  for k in place_data ]
    gdata = [ item for row in gdata for item in row ]
    numberCols = len(data["distance_data"]) + 2*len(gdata)
    
    # define time variables for places
    for keyword in data["place_data"]:
        lb = time_constraints[keyword]
        ub = data["user_data"]["bounds"][keyword]
        for place in data["place_data"][keyword]:
            tVar = LpVariable("x{}".format(curr_int), 0, float(ub), LpContinuous)
            tEntry = (tVar, keyword, place["price_level"])
            timeArray.append(tEntry)
            var_mapping[tVar.name] = place["name"]
            curr_int += 1

            if place["name"] == "HOME":
                dVar = LpVariable("x{}".format(curr_int), 1, 1, LpBinary)
            else:
                dVar = LpVariable("x{}".format(curr_int), 0, 1, LpBinary) 
            dEntry = (dVar, keyword, place["price_level"])
            decisionArray.append(dEntry)
            var_mapping[dVar.name] = place["name"]
            curr_int += 1

    for k in data["distance_data"]:
        frm, to = k
        dVar = LpVariable("x{}".format(curr_int), 0, 1, LpBinary)
        dEntry = (dVar, data["distance_data"][k])
        edgeArray.append(dEntry)
        var_mapping[dVar.name] = "{}, {}".format(frm, to)
        curr_int += 1

def addObjectiveFunction(data, timeArray, decisionArray, edgeArray, lp):
    # function to set the objective function
    tuples = []
    for (x, k, p) in timeArray:
        for keyword in data["place_data"]:
            for place in data["place_data"][keyword]:
                if (var_mapping[x.name] == place["name"]):
                    tuples.append((x, place["rating"]))

    lp += sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[0], decisionArray)) + -1*sum(map(lambda x: x[0]*x[1], edgeArray))

def addBudgetConstraint(data, decisionArray, lp):
    # function to add the budget constraint
    budget = data["user_data"]["budget"]
    lp += (sum(map(lambda x: x[0]*(x[2]-budget), decisionArray)) <= 0)
            

def addPathConstraint(data, decisionArray, edgeArray, lp):
    # function to add the IN-OUT constraints
    for (x, k, p) in decisionArray:
        nodeName = var_mapping[x.name]
        inBound = []
        outBound = []

        for (y, t) in edgeArray:
            frm, to = var_mapping[y.name].split(',')
            if nodeName == frm.strip():
                outBound.append(y)
            elif nodeName == to.strip():
                inBound.append(y)
        
        # inbound constraint
        lp += (sum(inBound) - x == 0)
        
        # outbound constraint
        lp += (sum(outBound) - x == 0)

def addTimeConstraint(data, timeArray, edgeArray, lp):
    # function to add the maximum time constraint
    p1 = sum(map(lambda e: e[0], timeArray))
    p2 = sum(map(lambda e: e[0]*e[1], edgeArray))
    lp += (p1 + p2 - data["user_data"]["time"]) <= 0
     
    

def addHomeConstraints(data, timeArray, decisionArray, lp):
    # function to add constraints about the Home node
    home_time = None
    home_d = None

    for (x, k, p) in timeArray:
        if (var_mapping[x.name] == "HOME"):
            home_time = x
            break

    for (x, k, p) in decisionArray:
        if (var_mapping[x.name] == "HOME"):
            home_d = x
            break
    
    lp += home_time == 0
    lp += home_d == 1

def addDecisionConstraints(data, timeArray, decisionArray, lp):
    # function to add constraints defining decision variable behavior
    tuples = []
    for (x, k, p) in timeArray:
        for (y, l, q) in decisionArray:
            if (var_mapping[x.name] == var_mapping[y.name]):
                tuples.append((x, y, k))
                break

    for (x, y, k) in tuples: 
        lowerBound = time_constraints[k]
        c1 = y*lowerBound - x <= 0
        lp += c1
        c2 = x - y*x.upBound <= 0
        lp += c2

def collectSubtours(edgeArray):
    tours = []
    edgeCopy = [ k for k in edgeArray if value(k[0])] 
   
    for edge in edgeCopy:

        original = var_mapping[edge[0].name].split(",")[0].strip()

        last = var_mapping[edge[0].name].split(",")[1].strip()

        inTour = False
        for subtour in tours:
            for node in subtour:
                if original == node or last == node:
                    inTour = True
                    break
            if inTour:
                break
                
        if inTour:
            continue

        subtour = []         

        subtour.append(original)

        while last != original:
            seen = False
            for e in edgeCopy:
                frm = var_mapping[e[0].name].split(",")[0].strip()
                to = var_mapping[e[0].name].split(",")[1].strip()

                if frm == last:
                    subtour.append(last)
                    last = to
                    seen = True
                    break
            if not seen:
                print(tours)
                print(subtour)
                exit(0)

        tours.append(subtour)
    return tours

def addSubtourConstraint(data, subtour, edgeArray, lp):    
    inBound = []
    outBound = []
    for nodeName in subtour:
        for (x, t) in edgeArray:
            frm = var_mapping[x.name].split(",")[0].strip()
            to = var_mapping[x.name].split(",")[1].strip()
        
            if to == nodeName and frm not in subtour:
                inBound.append(x)
            elif frm == nodeName and to not in subtour:
                outBound.append(x)
    nconst = sum(inBound) + sum(outBound) >= 2
    lp += nconst

def addKeywordConstraints(data, decisionArray, keywordArray, lp):
    for (keyword, equality, value) in keywordArray:
        associated_vars = []
        for (x, k, p) in decisionArray:
            if k == keyword:
                associated_vars.append(x)
        if (len(associated_vars) > 0):
            if equality == "EQ":
                lp += sum(associated_vars)  == value
            elif equality == "GTE":
                lp += sum(associated_vars)  >= value
            elif equality == "LTE":
                lp += sum(associated_vars)  <= value
        else:
            if equality != "LTE":
                badVar = LpVariable("bad", 0, None, LpInteger)
                lp += badVar <= 0
                lp += badVar >= 1
                print("adding infeasible route constraint")
                return
