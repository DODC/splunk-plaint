import os
import sys
import subprocess
import csv
import json

def main():
    unwrap_path = 'PATH TO abuse_ipdb_unwrap.py'
    _NEW_PYTHON_PATH = 'PATH TO PYTHON WITH REQUIRED MODULES FOR abuse_ipdb_unwrap.py'
    _SPLUNK_PYTHON_PATH = os.environ['PYTHONPATH']
    os.environ['PYTHONPATH'] = _NEW_PYTHON_PATH 
    IP = sys.argv[1]
    if IP == None:
        print('Incorrect Lookup IPADDRESS for ABUSEIPDB')
        sys.exit(0)
    COUNTRY = sys.argv[2]
    COUNTRY_CODE = sys.argv[3]
    FIRST_SEEN = sys.argv[4]
    LAST_SEEN = sys.argv[5]
    LATEST_REPORT = sys.argv[6]
    WHITE_LIST = sys.argv[7]
    TOTAL_REPORTS = sys.argv[8]
    infile = sys.stdin
    outfile = sys.stdout
    r = csv.DictReader(infile)
    w = csv.DictWriter(outfile, fieldnames=['IP','COUNTRY','COUNTRY_CODE',
                                            'FIRST_SEEN','LAST_SEEN','LATEST_REPORT',
                                            'WHITE_LIST','TOTAL_REPORTS'])
    w.writeheader()
    for result in r:
        my_process = os.path.join(os.getcwd(), unwrap_path)
        p = subprocess.Popen([os.environ['PYTHONPATH'], my_process, _SPLUNK_PYTHON_PATH, result[IP]], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = str(p.communicate()[0])
        j_output = output.replace("'", "\"")
        d_output = json.loads(j_output)
        result[COUNTRY] = d_output['COUNTRY']
        result[COUNTRY_CODE] = d_output['COUNTRY_CODE']
        result[FIRST_SEEN] = d_output['FIRST_SEEN']
        result[LAST_SEEN] = d_output['LAST_SEEN']
        result[LATEST_REPORT] = d_output['LATEST_REPORT']
        result[WHITE_LIST] = d_output['WHITE_LIST']
        result[TOTAL_REPORTS] = d_output['TOTAL_REPORTS']
        w.writerow(result)
        



if __name__ == '__main__':
    main()
