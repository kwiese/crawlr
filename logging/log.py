import datetime

logfilename = "/var/log/crawlr/crawlr.log"
perffilename = "/var/log/crawlr/perf.log"

def log(data):
    entry = "{}\n".format(data)
    of = open(logfilename, 'a+')
    of.write(entry)
    of.close()

def plog(data):
    tailer = "{}\n".format(("-"*47))
    header = "{}{}{}\n".format(("~"*10), str(datetime.datetime.now()), ("~"*10))
    of = open(perffilename, 'a+')
    of.write(header)
    for label, d in data:
        entry = "{}: {}\n".format(label, d)
        of.write(entry)
    of.write(tailer)
    of.close()
