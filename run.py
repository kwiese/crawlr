import os
#os.environ["GUROBI_HOME"] = "/opt/gurobi701/linux64"
#os.environ["PATH"] = os.environ["PATH"] + ":/opt/gurobi701/linux64/bin"
#try:
#    os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":/opt/gurobi701/linux64/lib"
#except KeyError:
#    os.environ["LD_LIBRARY_PATH"] = "/opt/gurobi701/linux64/lib"

os.system('source ./start_env')

from www.server import *

mapp = MyApp()
app.run(host='0.0.0.0', port=8002)
