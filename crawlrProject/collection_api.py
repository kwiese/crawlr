import json
import requests
import random

def collectData(data):
    url = getURL()
    response = requests.post(url, json=data)
    d = response.json()
    new_d = {}
    for k in d["distance_data"]:
        frm, to = k.split("__")
        new_k = (frm.rstrip(), to.rstrip())
        new_d[new_k] = d["distance_data"][k]
    d["distance_data"] = new_d
    
def getURL():
    return random.choice(URLS)
