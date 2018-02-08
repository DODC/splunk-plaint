import os
import sys
import csv
import gzip


def openany(p):
    if p.endswith(".gz"):
         return gzip.open(p)
    else:
         return open(p)

def do_work(field_value):
    print 'WORK IS DONE HERE'

event_count = sys.argv[2]  # NUMBER OF EVENTS RETURNED BY ALERT
results_file = sys.argv[3]      # FILE WITH RESULTS THAT WE WILL STEP THROUGH

try:
    for row in csv.DictReader(openany(results_file.replace('\r','/r').replace('\s','/s').replace('\v','/v').replace('\d','/d').replace('\p','/p').replace('\\','/'))):
         try:
            do_work(row["c_ip"]) # EXAMPLE WITH PULLING C_IP VALUE FROM RESULTS - CAN PULL ANY ROW NAME VALUE THAT IS PASSED FROM ALERT
         except:
            print 'Do Work Exception handling here'
except:
    print 'Exception handling for issue opening .gz results file'
