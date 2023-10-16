from dotenv import load_dotenv
load_dotenv()
import MySQLdb
import numpy as np


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

TABLE_NAME = 'SepPT_full'

cursor = connection.cursor()

def get_stat():
  cursor.execute(f"SELECT globalV_num, size, depth, circle_num FROM {TABLE_NAME};")
  res = cursor.fetchall()
  globalV_num_list = []
  size_list = []
  depth_list = []
  circle_num_list = []
  for entry in res:
    globalV_num_list.append(entry[0])
    size_list.append(entry[1])
    depth_list.append(entry[2])
    circle_num_list.append(entry[3])

  print('MEAN, MEDIAN, MAX, MIN')
  print(f'size:        {round(np.mean(size_list),1)}    {np.median(size_list)}    {max(size_list)}    {min(size_list)}')
  print(f'deth:        {round(np.mean(depth_list),1)}    {np.median(depth_list)}    {max(depth_list)}    {min(depth_list)}')
  print(f'circle_num:  {round(np.mean(circle_num_list),1)}    {np.median(circle_num_list)}    {max(circle_num_list)}    {min(circle_num_list)}')
  print(f'globalV_num: {round(np.mean(globalV_num_list),1)}    {np.median(globalV_num_list)}    {max(globalV_num_list)}    {min(globalV_num_list)}')



if __name__ == '__main__':
  get_stat()


connection.close()

# CREATE TABLE Top100Libs SELECT * FROM AllLibs WHERE github_star >= 26219
