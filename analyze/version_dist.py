import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
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
cursor.execute("SELECT version_num, file_num FROM jslibs;")

res = cursor.fetchall()
version_num_list = []
file_num_list = []
for entry in res:
    version_num_list.append(entry[0])
    file_num_list.append(entry[1])


##绘制直方图
# plt.rcParams["font.sans-serif"]='SimHei'
# plt.rcParams['axes.unicode_minus']=False

plt.hist(x=file_num_list, bins=100,
        color="steelblue",
        edgecolor="black")

#添加x轴和y轴标签
plt.xlabel("version number")
plt.ylabel("library number")

#添加标题
plt.title("Library's version number Distribution")

#显示图形
plt.show()