import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
import datetime
import time
from dotenv import load_dotenv
load_dotenv()
import MySQLdb
import json

connection = MySQLdb.connect(
  host= 'us-east.connect.psdb.cloud',
  user='yain51suytl8vm1cm4b2',
  passwd= 'pscale_pw_pEiVDtydTJqIpuJ68NRKenF0ncp6jjYipJkfxFDIHDN',
  db= 'js-lib-detect-trees',
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    #"ca": "/etc/ssl/cert.pem"   # For Mac
    "ca": "/etc/ssl/certs/ca-certificates.crt"  # For Linux
  }
)

cursor = connection.cursor()
cursor.execute("SELECT name, latest_version, latest_version_files FROM AccuLibs2;")

res = cursor.fetchall()

start = False
for entry in res:
    if entry[0] == 'ionic':
      start = True
    if not start:
      continue

    print(entry[0])
    for jsfile in json.loads(entry[2]):
      url = f'https://cdnjs.cloudflare.com/ajax/libs/{entry[0]}/{entry[1]}/{jsfile}'
      print(f"  {url}")
      res = urlopen(url)
      content = res.read()
      if not content:
        print('NO CONTENT')
    

connection.close()