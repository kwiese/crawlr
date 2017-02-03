import json
import requests
import random
import traceback
import unicodedata
import re
import urllib

from log import log

URLS = ["http://{}/query".format(line.rstrip()) for line in open('urls.txt', 'r')]

def collectData(data):
    try:
        url = getURL()
        log("using url {}".format(url))
        dt = json.dumps(data).encode('utf8')
        req = urllib.request.Request(url, data=dt, headers={'content-type': 'application/json'})
        f = urllib.request.urlopen(req)
        d = json.load(f) 
        new_d = {}
        for k in d["distance_data"]:
            frm, to = k.split("__")
            new_k = (frm.rstrip(), to.rstrip())
            new_d[new_k] = d["distance_data"][k]
        d["distance_data"] = new_d
        return d
    except Exception as e:
        log(traceback.format_exc())
    return {}
    
def getURL():
    return random.choice(URLS)
