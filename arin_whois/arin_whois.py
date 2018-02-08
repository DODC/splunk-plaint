import os
import sys
import subprocess
import csv
import json


def main():
    _NEW_PYTHON_PATH = 'c:/python27/python' # UPDATE THIS TO PATH OF PYTHON WITH CUSTOM MODULES REQUIRED 
    unwrap_path = 'PATH TO arin_whois_unwrap.py' # UPDATE THIS BEFORE IMPLEMENTATION
    _SPLUNK_PYTHON_PATH = os.environ['PYTHONPATH']
    os.environ['PYTHONPATH'] = _NEW_PYTHON_PATH 
    IP = sys.argv[1]
    if IP == None:
        print('Incorrect Lookup IPADDRESS for IPWHOIS')
        sys.exit(0)
    ASN = sys.argv[2]
    COUNTRY = sys.argv[3]
    ORG = sys.argv[4]
    infile = sys.stdin
    outfile = sys.stdout
    r = csv.DictReader(infile)
    w = csv.DictWriter(outfile, fieldnames=['IP','ASN','COUNTRY','ORG'])
    w.writeheader()
    for result in r:
        my_process = os.path.join(os.getcwd(), unwrap_path)
        p = subprocess.Popen([os.environ['PYTHONPATH'], my_process, _SPLUNK_PYTHON_PATH, result[IP]], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = str(p.communicate()[0])
        j_output = output.replace("'", "\"")
        d_output = json.loads(j_output)
        result[ASN] = d_output['asn']
        result[COUNTRY] = d_output['country']
        result[ORG] = d_output['org']
        w.writerow(result)

if __name__ == '__main__':
    main()        
