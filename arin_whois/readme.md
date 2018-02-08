# ARIN WHOIS Lookup using ipwhois Module

## Pre-reqs
1. Seperate python install on Splunk Search Head 
1. ipwhois python module on newly installed python
`pip install ipwhois` 

## Implementation 
* **Copy scripts to splunk/etc/apps/search/bin**
* **Update arin_whois.py**
   * `_NEW_PYTHON_PATH = 'c:/python27/python' # UPDATE THIS TO PATH OF SEPERATE PYTHON INSTALL WITH CUSTOM MODULES REQUIRED`
   * `unwrap_path = 'FULLPATH TO arin_whois_unwrap.py' # UPDATE THIS BEFORE IMPLEMENTATION - LOCATION WHERE YOU COPIED THESE SCRIPTS (likely splunk/etc/app/search/bin/arin_whois_unwrap.py)`
* **Add New 'Lookup Definition' in Splunk**
   * **In Splunk click Settings in upper right**
   * **Click Lookups** 
   
   ![Lookups](https://www.actforit.com/wp/wp-content/uploads/2018/02/lookup.png)
   * **Click 'Add New'** 
   
   ![Addnew](https://www.actforit.com/wp/wp-content/uploads/2018/02/add-new.png)
   * **Enter the following values and click 'Save'** 
   
   ![Setup](https://www.actforit.com/wp/wp-content/uploads/2018/02/setup.png)
   * **Update lookup permissions as necessary**

## Usage
In Splunk search rename desired ip field to IP:
ex. `|rename src_ip as IP`


Pass to sans_ds lookup with the following syntax:
`|lookup arin_whois IP as IP OUTPUT ASN COUNTRY ORG`


Output with table:
` | table IP,ASN,COUNTRY,ORG`

## Sample Output
![Sample](https://www.actforit.com/wp/wp-content/uploads/2018/02/sample.png)
