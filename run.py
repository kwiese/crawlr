
URLS = [k for k in open('urls.txt', 'r')]

from www.server import *

mapp = MyApp()
app.run(host='0.0.0.0', port=8002)
