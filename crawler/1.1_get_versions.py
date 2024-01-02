# Crawl all libraries and their Github star number from Cdnjs

from urllib.request import Request, urlopen
import json
import pandas as pd
import time
import MySQLdb

# Github API rate limit: 5000/hr
# Token generation: https://github.com/settings/tokens
GITHUB_TOKEN = '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'
OUTPUT_TABLE = 'libs_cdnjs'

connection = MySQLdb.connect(
    host= '127.0.0.1',
    user='root',
    passwd= '12345678',
    db= 'Libraries',
    autocommit = True
)
cursor = connection.cursor()

cursor.execute(f"SELECT `libname` FROM `{OUTPUT_TABLE}`;")
res = cursor.fetchall()

cnt = 1
for entry in res:
    libname = entry[0]
    res = urlopen(f'https://api.cdnjs.com/libraries/{libname}')
    lib_info = json.loads(res.read())
    version_list = lib_info['versions']
    version_num = 0
    latest_version = None
    if version_list and len(version_list) > 1:
        version_num = len(lib_info['versions'])
        latest_version = lib_info['versions'][-1]
    
    sql = f'''UPDATE `{OUTPUT_TABLE}` SET
            `#versions`=%s, `latest version`=%s WHERE libname=%s;'''
    val = (version_num, latest_version, libname)
    cursor.execute(sql, val)
    connection.commit() 
    print(f'{cnt} {libname}')
    cnt += 1