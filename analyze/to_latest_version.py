# Extract latest version of JS libs

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

TABLE_NAME = 'AccuLibs'

cursor = connection.cursor()
cursor.execute(f"SELECT name FROM {TABLE_NAME};")
libnames = cursor.fetchall()

cnt = 0
start = True
for entry in libnames:
    libname = entry[0]
    
    if start:
      cursor.execute(f"SELECT jsfiles, dev_jsfiles FROM {TABLE_NAME} WHERE name = '{libname}';")
      res = cursor.fetchone()
      file_collection = json.loads(res[0])

      latest_files = []
      latest_version = ''
      # Iterate through versions larger than '1.0.0'
      for i in range(len(file_collection)-1, -1, -1):
        files = file_collection[i][1]
        if len(files) > 0:
          latest_version = file_collection[i][0]
          latest_files = files
          break

      # Iterate through versions smaller than '1.0.0'
      if len(latest_files) == 0 and res[1] != None:
        dev_file_collection = json.loads(res[1])
        for i in range(len(dev_file_collection)-1, -1, -1):
          files = dev_file_collection[i][1]
          if len(files) > 0:
            latest_version = dev_file_collection[i][0]
            latest_files = files
            break

      sql = f"UPDATE {TABLE_NAME} SET latest_version_files = %s, latest_version_file_number = %s, latest_version = %s WHERE name = %s;"
      val = (json.dumps(latest_files), len(latest_files), latest_version, libname)
      cursor.execute(sql, val)
      connection.commit()

      cnt += 1
      print(f'{cnt}: {libname} updated.')

    # if libname == 'echarts-gl':
    #   start = True
    

connection.close()

# CREATE TABLE `AllLibs` (
# 	`name` varchar(255) NOT NULL,
# 	`version_num` int,
# 	`jsfile_num` int,
# 	`description` varchar(512),
# 	`jsfiles` json,
# 	`url` varchar(255),
# 	`latest_version_files` json,
# 	`latest_version_file_number` int,
# 	`github_star` int,
# 	`dev_jsfiles` json,
# 	`dev_jsfile_num` int,
# 	`dev_version_num` int,
# 	PRIMARY KEY (`name`)
# )