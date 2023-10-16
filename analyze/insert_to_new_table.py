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

with open('data/accuracy_libs.json', 'r') as openfile:
  lib_list = json.load(openfile)

print(len(lib_list))

for lib in lib_list:
  print(lib)
  cursor.execute(f"INSERT INTO AccuLibs SELECT * FROM AllLibs WHERE name='{lib}';")
  connection.commit()

connection.close()

# CREATE TABLE Top100Libs SELECT * FROM AllLibs WHERE github_star >= 26219
