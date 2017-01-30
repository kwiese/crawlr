#!/usr/bin/python
""" Setup script for the Gurobi optimizer
"""

# This script installs the gurobi module in your local environment, allowing
# you to say 'import gurobipy' from the Python shell.
#
# To install the Gurobi libraries, type 'python setup.py install'.  You
# may need to run this as superuser on a Linux system.
#
# We are grateful to Stuart Mitchell for his help with this script.

from distutils.core import setup #, Extension
import os,sys

License = """
    This software is covered by the Gurobi End User License Agreement.
    By completing the Gurobi installation process and using the software,
    you are accepting the terms of this agreement.
"""
version = sys.version_info[0:2]
if version != (2, 7) and version != (3, 5):
  raise RuntimeError("Unsupported Python version")

if os.name == 'posix':
  if sys.platform == 'darwin':
    version = 'python'+str(sys.version_info[0])+'.'+str(sys.version_info[1])
    srcpath = os.path.join('/opt/gurobi701/linux64/lib', version, 'gurobipy')
  else:
    version = 'python'+str(sys.version_info[0])+'.'+str(sys.version_info[1])
    if sys.maxunicode <= 1<<16:
      version = version+'_utf16'
    else:
      version = version+'_utf32'
    srcpath = os.path.join('/opt/gurobi701/linux64/lib', version, 'gurobipy')
  srcfile = 'gurobipy.so'
elif os.name == 'nt':
  version = 'python'+str(sys.version_info[0])+str(sys.version_info[1])
  srcpath = os.path.join(version, 'lib', 'gurobipy')
  srcfile = 'gurobipy.pyd'
else:
  raise RuntimeError("Unsupported operating system")

setup(name="gurobipy",
      version="7.0.1",
      description="""
    The Gurobi optimization engines represent the next generation in
    high-performance optimization software.
    """,
      license = License,
      url="http://www.gurobi.com/",
      author="Gurobi Optimization, Inc.",
      packages = ['gurobipy'],
      package_dir={'gurobipy' : srcpath },
      package_data = {'gurobipy' : [srcfile] }
      )

if sys.platform == 'darwin':
  from distutils.sysconfig import get_python_lib
  import subprocess
  import os.path
  sitelib = get_python_lib() + '/gurobipy/gurobipy.so'
  subprocess.call(('install_name_tool', '-change', 'libgurobi70.so', '/Library/gurobi700/mac64/lib/libgurobi70.so', sitelib)) # version for change
  default = '/System/Library/Frameworks/Python.framework/Versions/2.7/Python'
  modified = sys.prefix + '/Python'
  if default != modified:
    if not os.path.isfile(modified):
      modified = sys.prefix + '/lib/libpython2.7.dylib' # For Anaconda
    subprocess.call(('install_name_tool', '-change', default, modified, sitelib))
