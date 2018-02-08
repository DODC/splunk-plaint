import os
import sys
import subprocess
import csv
import json


def main():
    _NEW_PYTHON_PATH = 'c:/python27/python'
    _SPLUNK_PYTHON_PATH = os.environ['PYTHONPATH']
    os.environ['PYTHONPATH'] = _NEW_PYTHON_PATH 
    IP = sys.argv[1]
    if IP == None:
        print('Incorrect Lookup IPADDRESS for SANS_DS')
        sys.exit(0)
    COUNT = sys.argv[2]
    ATTACKS = sys.argv[3]
    MAXDATE = sys.argv[4]
    MINDATE = sys.argv[5]
    UPDATED = sys.argv[6]
    COMMENT = sys.argv[7]
    MAXRISK = sys.argv[8]
    ASABUSECONTACT = sys.argv[9]
    ASNUM = sys.argv[10]
    ASNAME = sys.argv[11]
    ASCOUNTRY = sys.argv[12]
    ASSIZE = sys.argv[13]
    NETWORK = sys.argv[14]
    THREATFEEDS = sys.argv[15]
    infile = sys.stdin
    outfile = sys.stdout
    r = csv.DictReader(infile)
    w = csv.DictWriter(outfile, fieldnames=['IP','COUNT','ATTACKS',
                                            'MAXDATE','MINDATE','UPDATED',
                                            'COMMENT','MAXRISK','ASABUSECONTACT',
                                            'ASNUM','ASNAME','ASCOUNTRY',
                                            'ASSIZE','NETWORK','THREATFEEDS'])
    w.writeheader()
    for result in r:
        my_process = os.path.join(os.getcwd(), 'd:/Program Files/Splunk/etc/apps/search/bin/sans_ds_unwrap.py')
        p = subprocess.Popen([os.environ['PYTHONPATH'], my_process, _SPLUNK_PYTHON_PATH, result[IP]], 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = str(p.communicate()[0])
        j_output = output.replace("'", "\"")
        d_output = json.loads(j_output)
        result[COUNT] = d_output['COUNT']
        result[ATTACKS] = d_output['ATTACKS']
        result[MAXDATE] = d_output['MAXDATE']
        result[MINDATE] = d_output['MINDATE']
        result[UPDATED] = d_output['UPDATED']
        result[COMMENT] = d_output['COMMENT']
        result[MAXRISK] = d_output['MAXRISK']
        result[ASABUSECONTACT] = d_output['ASABUSECONTACT']
        result[ASNUM] = d_output['ASNUM']
        result[ASNAME] = d_output['ASNAME']
        result[ASCOUNTRY] = d_output['ASCOUNTRY']
        result[ASSIZE] = d_output['ASSIZE']
        result[NETWORK] = d_output['NETWORK']
        result[THREATFEEDS] = d_output['THREATFEEDS']
        w.writerow(result)

if __name__ == '__main__':
    main()        
