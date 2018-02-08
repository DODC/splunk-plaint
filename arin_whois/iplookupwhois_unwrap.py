import csv
import sys
from ipwhois import IPWhois


def main():
    IP = sys.argv[2]
    output = {'IP':IP}
    obj = IPWhois(IP)
    results = obj.lookup_whois()
    try:
        output['asn'] = results['asn']
    except:
        output['asn'] = 'Not Found'
    try:
        output['country'] = results['asn_country_code']
    except:
        output['country'] = 'Not Found'
    try:
        output['org'] = results['asn_description'].replace(',','')
    except:
        output['org'] = 'Not Found'
    print output
    

if __name__ == '__main__':
    main()        

    
        
    

