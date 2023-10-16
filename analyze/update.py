from dotenv import load_dotenv
load_dotenv()
import MySQLdb


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

def update_lib_file_no():
  cursor.execute(f"SELECT libname FROM DetectLib;")
  libs = cursor.fetchall()
  for entry in libs:
      libname = entry[0]
      cursor.execute(f"SELECT count(*) FROM DetectFile WHERE libname='{libname}';")
      res = cursor.fetchone()
      cursor.execute(f"UPDATE DetectLib SET file_no={res[0]} WHERE libname='{libname}';")
      connection.commit()

def sum_lib_file_no():
  cnt = 0
  cursor.execute(f"SELECT file_no FROM DetectLib;")
  libs = cursor.fetchall()
  for entry in libs:
    cnt += entry[0]
  print(cnt)

def reset_id(table_name):
  cursor.execute(f"SELECT filename, id FROM {table_name} ORDER BY libname;")
  res = cursor.fetchall()
  for entry in res:
    cursor.execute(f"UPDATE {table_name} SET id = {entry[1] + 1000} where filename = '{entry[0]}';")
    connection.commit()
  cnt = 0
  for entry in res:
    cnt += 1
    cursor.execute(f"UPDATE {table_name} SET id = {cnt} where filename = '{entry[0]}';")
    connection.commit()
  

if __name__ == '__main__':
  reset_id('DetectFile')


connection.close()

# CREATE TABLE Top100Libs SELECT * FROM AllLibs WHERE github_star >= 26219
