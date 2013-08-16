from distutils.core import setup
import py2exe, os, sys

mypath = os.path.normpath(os.path.dirname(os.path.abspath(sys.argv[0])))

setup(console=[os.path.join(mypath, "CLIENTCLIW.py")])