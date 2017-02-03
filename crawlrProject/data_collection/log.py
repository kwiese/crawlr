import datetime
import grequests

url = ["http://{}:5000".format(line.rstrip()) for line in open('logurl.txt', 'r')]
logurl = "{}/event".format(url[0])
perfurl = "{}/perf".format(url[0])
badfile = "/var/log/crawlr/crawlr.log"

def log_local(data):
    entry = "{}: {}\n".format(str(datetime.datetime.now()), data)
    of = open(badfile, 'a+')
    of.write(entry)
    of.close()

def log(data):
    entry = "{}: {}".format(str(datetime.datetime.now()), data)
    packet = {"payload": entry}
    try:
        req = grequests.post(logurl, json=packet)
        j = grequests.map([req])
        log_local(j)
    except Exception as e:
        log_local(traceback.format_exc())

def perf(pairs):
    packet = {"payload": pairs}
    try:
        req = grequests.post(perfurl, json=packet)
        j = grequests.map([req])
        log_local(j)
    except Exception as e:
        log_local(traceback.format_exc())
