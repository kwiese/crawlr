import datetime

logfilename = "/var/log/crawlr/crawlr.log"

def log(data):
    entry = "{}: {}\n".format(str(datetime.datetime.now()), data)
    of = open(logfilename, 'a+')
    of.write(entry)
    of.close()
