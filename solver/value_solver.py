"""
Authors: Sean Donohoe and Kyle Wiese

An implementation for composing and solving the linear program, using the PuLP API
"""

from gurobipy import *
from bounds import time_constraints
from log import log, perf
from solver.fastcode.collection import collectSubtoursFast, collectRelated
from threading import Lock

import traceback
import time
import random

env = Env.CloudEnv("cloud.log", "e3f97d2a-b91d-4da1-ae3d-ad13cd9079d3", "NBFaCx9pQtOe84vWzikcBA", "")
lastUsed = time.time()
envGuard = Lock()

class FuckedException(Exception):
    pass

def checkEnv():
    global lastUsed
    global env
    envGuard.acquire()
    try:
        if (time.time() - lastUsed) >= 10800:
            env = Env.CloudEnv("cloud.log", "e3f97d2a-b91d-4da1-ae3d-ad13cd9079d3", "NBFaCx9pQtOe84vWzikcBA", "")
            lastUsed = time.time()
        else:
            lastUsed = time.time()
    finally:
        envGuard.release()

def cascade(data, var_mapping, subtourCount):
    timeArray = []
    decisionArray = []
    edgeArray = []
    keywordArray = []
    subtourArray = []
    
    checkEnv()
    lp = Model("value optimizer", env=env)
    lp.setParam("OutputFlag", False)
    
    initialize(lp, data, timeArray, decisionArray, edgeArray, keywordArray, var_mapping)

    addBudgetConstraint(data, decisionArray, lp, var_mapping)   
   
    addPathConstraint(data, decisionArray, edgeArray, lp, var_mapping)

    addTimeConstraint(data, timeArray, edgeArray, lp, var_mapping)

    addHomeConstraints(data, timeArray, decisionArray, lp, var_mapping)

    addDecisionConstraints(data, timeArray, decisionArray, lp, var_mapping) 

    addKeywordConstraints(data, decisionArray, keywordArray, lp, var_mapping)
    if True:
        lp.update()
        pre = time.time()
        addPreEmptiveConstraints(data, edgeArray, decisionArray, subtourArray, lp, var_mapping, subtourCount)
        log("Time to add preemptive: {}".format((time.time() - pre)))

    addObjectiveFunction(data, timeArray, decisionArray, edgeArray, subtourArray, lp, var_mapping)
    lp.update()

    return (subtourArray, timeArray, decisionArray, edgeArray, keywordArray, lp)

def solve(data):
    subtourCount = 1
    var_mapping = {}
    sdatac = 0
    sdata = 0
    cdatac = 0
    cdata = 0
    cnsdatac = 0
    cnsdata = 0
    iters = 1
    
    try:
        (subtourArray, timeArray, decisionArray, edgeArray, keywordArray, lp) = cascade(data, var_mapping, subtourCount)
    except Exception as e:
        log(traceback.format_exc())
        raise e

    log("After cascade")
    
    sopt = time.time()
    try:
        t = time.time()
        lp.optimize()
        sdatac += 1
        sdata += (time.time() - t)
    except Exception as e:
        log(traceback.format_exc())
        raise e

    log(lp.Status)

    pdata = []
    stn = []
    stl = []
    c = time.time()
    subtours = collectSubtours(edgeArray, lp, var_mapping)
    cdatac += 1
    cdata += (time.time() - c)
    tuned = False
    while len(subtours) > 1:
        stn.append(len(subtours))
        for subtour in subtours:
            if "HOME" not in subtour:
                stl.append(len(subtour))
                ct = time.time()
                addSubtourConstraint(data, subtour, edgeArray, decisionArray, subtourArray, lp, var_mapping, subtourCount)
                cnsdatac += 1
                cnsdata += (time.time() - ct)
        addObjectiveFunction(data, timeArray, decisionArray, edgeArray, subtourArray, lp, var_mapping)
        t = time.time()
        lp.optimize()
        iters += 1
        sdatac += 1
        sdata += (time.time() - t)
        c = time.time()
        subtours = collectSubtours(edgeArray, lp, var_mapping)
        cdatac += 1
        cdata += (time.time() - c)
    eopt = time.time()
    log("Solution found!")
    pdata.append(("Number of places", len(decisionArray)))
    if len(stn):
        pdata.append(("Average number of subtours per iteration", (sum(stn)/len(stn))))
    if len(stl):
        pdata.append(("Average subtour length", (sum(stl)/len(stl))))
    if cdatac:
        pdata.append(("Average time to collect subtours", (cdata/cdatac)))
        pdata.append(("Time to collect subtours", cdata))
    if cnsdatac:
        pdata.append(("Time to add constraints", cnsdata))
        pdata.append(("Average time to add constraints", (cnsdata/cnsdatac)))
    pdata.append(("Total iterations", iters))
    if sdatac:
        pdata.append(("Average time to solve a problem instance", (sdata/sdatac)))
    pdata.append(("Time to solve", (eopt - sopt)))
    perf(pdata)

    chosenEdges = []
    
    for (frm, to, en, t) in edgeArray:
        if en.X:
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
    log("returning data")
    return rdata

def initialize(lp, data, timeArray, decisionArray, edgeArray, keywordArray, var_mapping):
    # function to initialize the columns and rows of the problem
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
            tVar = lp.addVar(vtype=GRB.CONTINUOUS, name="x{}".format(curr_int), lb=0, ub=float(ub))
            tEntry = ("x{}".format(curr_int), tVar, keyword, place["price_level"], float(ub))
            timeArray.append(tEntry)
            var_mapping[tEntry[0]] = place["name"]
            curr_int += 1

            dVar = lp.addVar(vtype=GRB.BINARY, name="x{}".format(curr_int))
            dEntry = ("x{}".format(curr_int), dVar, keyword, place["price_level"])
            decisionArray.append(dEntry)
            var_mapping[dEntry[0]] = place["name"]
            curr_int += 1

    for k in data["distance_data"]:
        frm, to = k
        dVar = lp.addVar(vtype=GRB.BINARY, name="x{}".format(curr_int))
        dEntry = (frm, to, dVar, data["distance_data"][k])
        edgeArray.append(dEntry)
        var_mapping[dEntry[0]] = (frm, to)
        curr_int += 1

def addObjectiveFunction(data, timeArray, decisionArray, edgeArray, subtourArray, lp, var_mapping):
    # function to set the objective function
    tuples = []
    for (x, xn, k, p, ub) in timeArray:
        for keyword in data["place_data"]:
            for place in data["place_data"][keyword]:
                if (var_mapping[x] == place["name"]):
                    tuples.append((xn, place["rating"]))
    if len(subtourArray):
        lp.setObjective(sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[1], decisionArray)) + -1*sum(map(lambda x: x[2]*x[3], edgeArray)) + -1*sum(subtourArray), GRB.MAXIMIZE)
    else:
        lp.setObjective(sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[1], decisionArray)) + -1*sum(map(lambda x: x[2]*x[3], edgeArray)), GRB.MAXIMIZE)

def addBudgetConstraint(data, decisionArray, lp, var_mapping):
    # function to add the budget constraint
    budget = data["user_data"]["budget"]
    lp.addConstr(sum(map(lambda x: x[1]*(x[3]-budget), decisionArray)) <= 0, "budget")
            

def addPathConstraint(data, decisionArray, edgeArray, lp, var_mapping):
    # function to add the IN-OUT constraints
    for (x, xn, k, p) in decisionArray:
        nodeName = var_mapping[x]
        inBound = []
        outBound = []

        for (frm, to, yn, t) in edgeArray:
            if nodeName == frm.strip():
                outBound.append(yn)
            elif nodeName == to.strip():
                inBound.append(yn)
        
        # inbound constraint
        lp.addConstr(sum(inBound) - xn == 0, "path_inbound")
        
        # outbound constraint
        lp.addConstr(sum(outBound) - xn == 0, "path_outbound")

def addTimeConstraint(data, timeArray, edgeArray, lp, var_mapping):
    # function to add the maximum time constraint
    p1 = sum(map(lambda e: e[1], timeArray))
    p2 = sum(map(lambda e: e[2]*e[3], edgeArray))
    lp.addConstr(p1 + p2 - data["user_data"]["time"] <= 0, "time")

def addHomeConstraints(data, timeArray, decisionArray, lp, var_mapping):
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
    
    lp.addConstr(home_time == 0, "home_time")
    lp.addConstr(home_d == 1, "home_decision")

def addDecisionConstraints(data, timeArray, decisionArray, lp, var_mapping):
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
        lp.addConstr(y*lowerBound - x <= 0, "cd{}".format(curr_int))
        curr_int += 1
        lp.addConstr(x - y*ub <= 0, "cd{}".format(curr_int))
        curr_int += 1

def collectSubtours(edgeArray, lp, var_mapping):
    subtours = collectSubtoursFast(edgeArray, len(edgeArray))
    if len(subtours):
        return subtours
    else:
        log(edgeArray)
        raise FuckedException("everything is terrible")

def addSubtourConstraint(data, subtour, edgeArray, decisionArray, subtourArray, lp, var_mapping, subtourCount): 
    if "HOME" in subtour:
        return

    inBound, outBound = collectRelated(subtour, edgeArray)
    
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
    
    lp.addConstr(sum(nodes) - subti <= len(nodes) - 1, "subt_cons{}".format(subtourCount))

    lp.addConstr(subti - sum(inBound) <= 0, "subt_1in{}".format(subtourCount))

    lp.addConstr(subti - sum(outBound) <= 0, "subt_1out{}".format(subtourCount))

    subtourCount += 1

def addKeywordConstraints(data, decisionArray, keywordArray, lp, var_mapping):
    for (keyword, equality, value) in keywordArray:
        associated_vars = []
        for (x, xn, k, p) in decisionArray:
            if k == keyword:
                associated_vars.append(xn)
        if (len(associated_vars) > 0):
            if equality == "EQ":
                lp.addConstr(sum(associated_vars) == value, keyword)
            elif equality == "GTE":
                lp.addConstr(sum(associated_vars) >= value, keyword)
            elif equality == "LTE":
                lp.addConstr(sum(associated_vars) <= value, keyword)
        else:
            if equality != "LTE":
                badVar = lp.addVar(vtype=GRB.BINARY, name="bad")
                lp.addConstr(badVar <= 0, "b1")
                lp.addConstr(badVar >= 1, "b2")
                log("adding infeasible route constraint")
                return

def addPreEmptiveConstraints(data, edgeArray, decisionArray, subtourArray, lp, var_mapping, subtourCount):
    gdata = [ var_mapping[y]  for (y, yn, k, p) in decisionArray if var_mapping[y] != "HOME" ]
    choose_3 = []
    for (frm, to, en, t) in edgeArray:
        if frm == "HOME":
            choose_3.append((to, t))
    choose_3.sort(key=lambda x: x[1])

#    b = int(len(choose_3)/3)
    b = int(len(choose_3)/4)
#    choose_3 = choose_3[-b:]
#    choose_3 = choose_3[b:2*b]
#    choose_3 = choose_3[b:]
    choose_3 = choose_3[b:3*b]
    
    for i in range(len(gdata)):
        frm = gdata[i]
        for j in range(i+1, len(gdata)):
            addSubtourConstraint(data, [frm, gdata[j]], edgeArray, decisionArray, subtourArray, lp, var_mapping, subtourCount)

    for i in range(len(choose_3)):
        f,tf = choose_3[i]
        for j in range(i+1, len(choose_3)):
            s,sf = choose_3[j]
            for k in range(j+1, len(choose_3)):
                th,thf = choose_3[k]
                addSubtourConstraint(data, [f, s, th], edgeArray, decisionArray, subtourArray, lp, var_mapping, subtourCount)
