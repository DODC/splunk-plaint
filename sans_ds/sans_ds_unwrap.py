from lxml import etree
import urllib2
import sys

IP = str(sys.argv[2])
output = {'IP':IP}
base_url = 'http://isc.sans.edu/api/ip/'
sans_data = urllib2.urlopen(base_url + IP).read()
root = etree.fromstring(sans_data)
for entry in root:
    if entry.tag == 'number':
        pass
    elif entry.tag == 'threatfeeds':
        feedcount = 0
        for item in entry.iterchildren():
            feedcount+=1
        output[str(entry.tag).upper()] = str(feedcount)
    elif entry.tag == 'as':
        output['ASNUM'] = str(entry.text).replace(',','')
    else:
        output[str(entry.tag).upper()] = str(entry.text).replace(',','')
if 'THREATFEEDS' not in output:
    output['THREATFEEDS'] = '0'
    
print output
