import requests
import sqlite3
import json
import sys
from datetime import datetime
from sqlite3 import Error


def create_con(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print e
        
    return None

def create_table(conn, sql_com):
    try:
        c = conn.cursor()
        c.execute(sql_com)
    except Error as e:
        print e

def select_all_data(conn,value):
    c = conn.cursor()
    c.execute("SELECT * FROM iplookup where ip_address")
    rows = c.fetchall()
    for row in rows:
        print row
    return len(rows)

def select_ip(conn,value):
    c = conn.cursor()
    c.execute("SELECT * FROM iplookup where ip_address=?", (value,))
    rows = c.fetchall()
    return rows

def insert_data(conn, data):
    sql = """ INSERT INTO iplookup(ip_address,country,country_code,first_seen,last_seen,latest_report,white_list,total_reports)
              VALUES(?,?,?,?,?,?,?,?)"""
    c = conn.cursor()
    c.execute(sql, data)
    return c.lastrowid

def update_data(conn,row_id,data):
    final_data = (data, row_id)
    sql = """ UPDATE iplookup SET last_seen = ? WHERE id = ?"""
    c = conn.cursor()
    c.execute(sql, final_data)
    conn.commit()
    
    

def api_req(IP,api_key):
    request = 'https://www.abuseipdb.com/check/%s/json?key=%s' % (IP, api_key)
    r = requests.get(request)
    result = {}
    try:
        data = r.json()
        if not data:
            print 'No Data Returned'
        else:
            result['total_reports'] = len(data)
            result['country'] = data[0]['country']
            result['country_code'] = data[0]['isoCode']
            result['latest_report'] = data[0]['created']
            if data[0]['isWhitelisted'] == True:
                result['white_list'] = 1
            else:
                result['white_list'] = 0
        return result
    except:
        print 'Failed to get data'





IP = str(sys.argv[2])
api_key = 'ABUSEIPDB.COM APIKEY HERE'
sql_create_iplookup_table = """CREATE TABLE IF NOT EXISTS iplookup (
                                    id integer PRIMARY KEY,
                                    ip_address text NOT NULL,
                                    country text NOT NULL,
                                    country_code text NOT NULL,
                                    first_seen text NOT NULL,
                                    last_seen text NOT NULL,
                                    latest_report text NOT NULL,
                                    white_list integer NOT NULL,
                                    total_reports integer NOT NULL
                                );"""

sql_lite = 'abuse_ipdb.db'
db_conn = create_con(sql_lite)
cur_time = str(datetime.now())
if db_conn is not None:
    create_table(db_conn, sql_create_iplookup_table)
db_conn.close()
db_conn = create_con(sql_lite)
output = {'IP':IP}
exist_data = select_ip(db_conn,IP)
if len(exist_data) > 0:
    found_id = exist_data[0][0]
    update_data(db_conn, found_id, cur_time)
else:
    lookup = api_req(IP,api_key)
    if len(lookup) > 0:
        add_data = (IP,lookup['country'],lookup['country_code'],cur_time,cur_time,lookup['latest_report'],str(lookup['white_list']),lookup['total_reports'])
        res = insert_data(db_conn,add_data)
        db_conn.commit()
    else:
        add_data = (IP,'N/A','N/A',cur_time,cur_time,'N/A','N/A','N/A')
        res = insert_data(db_conn,add_data)
        db_conn.commit()
exist_data = select_ip(db_conn,IP)
db_conn.close()
output['COUNTRY'] = str(exist_data[0][2])
output['COUNTRY_CODE'] = str(exist_data[0][3])
output['FIRST_SEEN'] = str(exist_data[0][4])
output['LAST_SEEN'] = str(cur_time)
output['LATEST_REPORT'] = str(exist_data[0][6].replace(',',''))
if exist_data[0][7] == 1:
    output['WHITE_LIST'] = 'True'
elif exist_data[0][7] == 0:
    output['WHITE_LIST'] = 'False'
else:
    output['WHITE_LIST'] = str('N/A')
if exist_data[0][8] == 'N/A':
    output['TOTAL_REPORTS'] = str(exist_data[0][8])
else:
    output['TOTAL_REPORTS'] = exist_data[0][8]
print output



