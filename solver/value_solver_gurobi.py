"""
Authors: Sean Donohoe and Kyle Wiese

An implementation for composing and solving the linear program, using the PuLP API
"""


# from pulp import *
from gurobipy import *
from www.bounds import time_constraints

var_mapping = {}
env = Env.CloudEnv("cloud.log", "e3f97d2a-b91d-4da1-ae3d-ad13cd9079d3", "NBFaCx9pQtOe84vWzikcBA", "")
subtourCount = 1

def cascade(data):
    timeArray = []
    decisionArray = []
    edgeArray = []
    keywordArray = []

#    lp = LpProblem("value optimizer", LpMaximize)
    lp = Model("value optimizer", env=env)
    lp.setParam("OutputFlag", False)
    
    initialize(lp, data, timeArray, decisionArray, edgeArray, keywordArray)

    addBudgetConstraint(data, decisionArray, lp)   
   
    addPathConstraint(data, decisionArray, edgeArray, lp)

    addTimeConstraint(data, timeArray, edgeArray, lp)

    addHomeConstraints(data, timeArray, decisionArray, lp)

    addDecisionConstraints(data, timeArray, decisionArray, lp) 

    addKeywordConstraints(data, decisionArray, keywordArray, lp)

    addObjectiveFunction(data, timeArray, decisionArray, edgeArray, [], lp)

    return (timeArray, decisionArray, edgeArray, keywordArray, lp)

def solve(data):
    global subtourCount
    global var_mapping
    subtourCount = 1
    var_mapping = {}
    
    (timeArray, decisionArray, edgeArray, keywordArray, lp) = cascade(data)
    subtourArray = []
    
#    status = lp.solve(GLPK(msg=0))
    lp.optimize()

    subtours = collectSubtours(edgeArray, lp)
    while len(subtours) > 1:
        print(len(subtours))
        print([ len(k) for k in subtours ])
        for subtour in subtours:
            addSubtourConstraint(data, subtour, edgeArray, decisionArray, subtourArray, lp)
        addObjectiveFunction(data, timeArray, decisionArray, edgeArray, subtourArray, lp)
        lp.update()
        lp.optimize()
        subtours = collectSubtours(edgeArray, lp)

    chosenEdges = []
    
    for (e, en, t) in edgeArray:
        if en.X:
            frm = var_mapping[e].split(",")[0].strip()
            to = var_mapping[e].split(",")[1].strip()
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
            for (y, yn, k, p, ub) in timeArray:
                if var_mapping[y] == last:
                    last_t = yn
                    key = k
                    break
            last_d = None
            for (y, yn, k, p) in decisionArray:
                if var_mapping[y] == last:
                    last_d = yn
                    break
            print("{}: time: {}, place decision: {}".format(last, last_t.X, last_d.X))
            la = None
            for place in data["place_data"][key]:
                if place["name"] == last:
                    pla = place
                    break
            time_s = last_t.X
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
            
    rdata = {
        "path": final_path,
        "addresses": final_addresses,
    }
    return rdata

def initialize(lp, data, timeArray, decisionArray, edgeArray, keywordArray):
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
#            tVar = LpVariable("x{}".format(curr_int), 0, float(ub), LpContinuous)
            tVar = lp.addVar(vtype=GRB.CONTINUOUS, name="x{}".format(curr_int), lb=0, ub=float(ub))
            tEntry = ("x{}".format(curr_int), tVar, keyword, place["price_level"], float(ub))
            timeArray.append(tEntry)
#            var_mapping[tVar.name] = place["name"]
            var_mapping[tEntry[0]] = place["name"]
            curr_int += 1

            if place["name"] == "HOME":
#                dVar = LpVariable("x{}".format(curr_int), 1, 1, LpBinary)
                 dVar = lp.addVar(vtype=GRB.BINARY, name="x{}".format(curr_int))
            else:
#                dVar = LpVariable("x{}".format(curr_int), 0, 1, LpBinary) 
                 dVar = lp.addVar(vtype=GRB.BINARY, name="x{}".format(curr_int))
            dEntry = ("x{}".format(curr_int), dVar, keyword, place["price_level"])
            decisionArray.append(dEntry)
#            var_mapping[dVar.name] = place["name"]
            var_mapping[dEntry[0]] = place["name"]
            curr_int += 1

    for k in data["distance_data"]:
        frm, to = k
#        dVar = LpVariable("x{}".format(curr_int), 0, 1, LpBinary)
        dVar = lp.addVar(vtype=GRB.BINARY, name="x{}".format(curr_int))
        dEntry = ("x{}".format(curr_int), dVar, data["distance_data"][k])
        edgeArray.append(dEntry)
#        var_mapping[dVar.name] = "{}, {}".format(frm, to)
        var_mapping[dEntry[0]] = "{}, {}".format(frm, to)
        curr_int += 1
    lp.update()

def addObjectiveFunction(data, timeArray, decisionArray, edgeArray, subtourArray, lp):
    # function to set the objective function
    tuples = []
    for (x, xn, k, p, ub) in timeArray:
        for keyword in data["place_data"]:
            for place in data["place_data"][keyword]:
                if (var_mapping[x] == place["name"]):
                    tuples.append((xn, place["rating"]))
    if len(subtourArray):
        lp.setObjective(sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[1], decisionArray)) + -1*sum(map(lambda x: x[1]*x[2], edgeArray)) + -1*sum(subtourArray), GRB.MAXIMIZE)
    else:
        lp.setObjective(sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[1], decisionArray)) + -1*sum(map(lambda x: x[1]*x[2], edgeArray)), GRB.MAXIMIZE)

def addBudgetConstraint(data, decisionArray, lp):
    # function to add the budget constraint
    budget = data["user_data"]["budget"]
#    lp += (sum(map(lambda x: x[0]*(x[2]-budget), decisionArray)) <= 0)
    lp.addConstr(sum(map(lambda x: x[1]*(x[3]-budget), decisionArray)) <= 0, "budget")
            

def addPathConstraint(data, decisionArray, edgeArray, lp):
    # function to add the IN-OUT constraints
    for (x, xn, k, p) in decisionArray:
#        nodeName = var_mapping[x.name]
        nodeName = var_mapping[x]
        inBound = []
        outBound = []

        for (y, yn, t) in edgeArray:
#            frm, to = var_mapping[y.name].split(',')
            frm, to = var_mapping[y].split(',')
            if nodeName == frm.strip():
                outBound.append(yn)
            elif nodeName == to.strip():
                inBound.append(yn)
        
        # inbound constraint
#        lp += (sum(inBound) - x == 0)
        lp.addConstr(sum(inBound) - xn == 0, "path_inbound")
        
        # outbound constraint
#        lp += (sum(outBound) - x == 0)
        lp.addConstr(sum(outBound) - xn == 0, "path_outbound")

def addTimeConstraint(data, timeArray, edgeArray, lp):
    # function to add the maximum time constraint
    p1 = sum(map(lambda e: e[1], timeArray))
    p2 = sum(map(lambda e: e[1]*e[2], edgeArray))
#    lp += (p1 + p2 - data["user_data"]["time"]) <= 0
    lp.addConstr(p1 + p2 - data["user_data"]["time"] <= 0, "time")

def addHomeConstraints(data, timeArray, decisionArray, lp):
    # function to add constraints about the Home node
    home_time = None
    home_d = None

    for (x, xn, k, p, ub) in timeArray:
        if (var_mapping[x] == "HOME"):
            home_time = xn
            break

    for (x, xn, k, p) in decisionArray:
        if (var_mapping[x] == "HOME"):
            home_d = xn
            break
    
#    lp += home_time == 0
    lp.addConstr(home_time == 0, "home_time")
#    lp += home_d == 1
    lp.addConstr(home_d == 1, "home_decision")

def addDecisionConstraints(data, timeArray, decisionArray, lp):
    # function to add constraints defining decision variable behavior
    tuples = []
    for (x, xn, k, p, ub) in timeArray:
        for (y, yn, l, q) in decisionArray:
            if (var_mapping[x] == var_mapping[y]):
                tuples.append((xn, yn, k, ub))
                break
    curr_int = 1
    for (x, y, k, ub) in tuples: 
        lowerBound = time_constraints[k]
#        c1 = y*lowerBound - x <= 0
#        lp += c1
        lp.addConstr(y*lowerBound - x <= 0, "cd{}".format(curr_int))
        curr_int += 1
#        c2 = x - y*x.upBound <= 0
#        lp += c2
        lp.addConstr(x - y*ub <= 0, "cd{}".format(curr_int))
        curr_int += 1

def collectSubtours(edgeArray, lp):
    tours = []
#    edgeCopy = [ k for k in edgeArray if value(k[0])] 
    edgeCopy = [ k for k in edgeArray if k[1].X ]
    print("edges collected")
    for edge in edgeCopy:

        original = var_mapping[edge[0]].split(",")[0].strip()

        last = var_mapping[edge[0]].split(",")[1].strip()

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
                frm = var_mapping[e[0]].split(",")[0].strip()
                to = var_mapping[e[0]].split(",")[1].strip()

                if frm == last:
                    subtour.append(last)
                    last = to
                    seen = True
                    break
            if not seen:
                print(tours)
                print(subtour)
                print(edge[0].VarName)
                print([ k[0].varName for k in edgeCopy ])
                # this should raise an error
                exit(0)

        tours.append(subtour)
    print("tours collected")
    return tours

def addSubtourConstraint(data, subtour, edgeArray, decisionArray, subtourArray, lp): 
    global subtourCount   
    inBound = []
    outBound = []
    skip = False
    for nodeName in subtour:
        if nodeName == "HOME":
            skip = True
            break
        for (x, xn, t) in edgeArray:
            frm = var_mapping[x].split(",")[0].strip()
            to = var_mapping[x].split(",")[1].strip()
            if to == nodeName and frm not in subtour:
                inBound.append(xn)
            elif frm == nodeName and to not in subtour:
                outBound.append(xn)
    
    if not skip:
        nodevars = [ 
            x for k in subtour
            for x in var_mapping
            if var_mapping[x] == k
        ]
        nodes = [
            k[1] for n in nodevars
            for k in decisionArray
            if n == k[0]
        ]
        subti = lp.addVar(vtype=GRB.BINARY, name="subt{}".format(subtourCount))
        subtourArray.append(subti)
        
        lp.addConstr(sum(nodes) - len(nodes)*subti == 0, "subt_cons{}".format(subtourCount))

        lp.addConstr(subti - sum(inBound) <= 0, "subt_1in{}".format(subtourCount))
        lp.addConstr(sum(inBound) - len(inBound)*subti <= 0, "subt_2in{}".format(subtourCount))

        lp.addConstr(subti - sum(outBound) <= 0, "subt_1out{}".format(subtourCount))
        lp.addConstr(sum(outBound) - len(outBound)*subti <= 0, "subt_2out{}".format(subtourCount))

        subtourCount += 1

def addKeywordConstraints(data, decisionArray, keywordArray, lp):
    for (keyword, equality, value) in keywordArray:
        associated_vars = []
        for (x, xn, k, p) in decisionArray:
            if k == keyword:
                associated_vars.append(xn)
        if (len(associated_vars) > 0):
            if equality == "EQ":
#                lp += sum(associated_vars)  == value
                lp.addConstr(sum(associated_vars) == value, keyword)
            elif equality == "GTE":
#                lp += sum(associated_vars)  >= value
                lp.addConstr(sum(associated_vars) >= value, keyword)
            elif equality == "LTE":
#                lp += sum(associated_vars)  <= value
                lp.addConstr(sum(associated_vars) <= value, keyword)
        else:
            if equality != "LTE":
#                badVar = LpVariable("bad", 0, None, LpInteger)
                badVar = lp.addVar(vtype=GRB.BINARY, name="bad")
#                lp += badVar <= 0
                lp.addConstr(badVar <= 0, "b1")
#                lp += badVar >= 1
                lp.addConstr(badVar >= 1, "b2")
                print("adding infeasible route constraint")
                return
