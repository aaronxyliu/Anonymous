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


for lib in lib_list:
  print(lib)
  cursor.execute(f"SELECT dev_jsfiles, dev_jsfile_num, dev_version_num FROM AllLibs WHERE name = '{lib}';")
  res = cursor.fetchone()
  sql = "UPDATE AccuLibs SET dev_jsfiles = %s, dev_jsfile_num = %s, dev_version_num = %s WHERE name = %s;"
  val = (res[0], res[1], res[2], lib)
  cursor.execute(sql, val)
  connection.commit()

connection.close()

# CREATE TABLE Top100Libs SELECT * FROM AllLibs WHERE github_star >= 26219
