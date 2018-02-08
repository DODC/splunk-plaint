import os
import sys
import subprocess

event_count = sys.argv[1]
results_file = sys.argv[8]
worker_script = 'YOUR WORKER SCRIPT FULL PATH HERE'

_NEW_PYTHON_PATH = 'c:/python27/python'
_SPLUNK_PYTHON_PATH = os.environ['PYTHONPATH']

os.environ['PYTHONPATH'] = _NEW_PYTHON_PATH 
my_process = os.path.join(os.getcwd(), worker_script)

p = subprocess.Popen([os.environ['PYTHONPATH'], my_process, _SPLUNK_PYTHON_PATH, event_count, results_file], 
stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = p.communicate()[0]
