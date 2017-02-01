import datetime
import grequests

logurl = ["http://{}:5000/event".format(line.rstrip()) for line in open('logurl.txt', 'r')]
logurl = logurl[0]
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
#        grequests.send(req, grequests.Pool(1))
        j = grequests.map([req])
        log_local(j)
    except Exception as e:
        log_local(traceback.format_exc())
