# Get github star using API

from urllib.request import Request, urlopen
from dotenv import load_dotenv
load_dotenv()
import MySQLdb
import json
import time

# Github API rate limit: 5000/hr
# Token generation: https://github.com/settings/tokens
GITHUB_TOKEN = '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'

connection = MySQLdb.connect(
  host= 'us-east.connect.psdb.cloud',
  user='yain51suytl8vm1cm4b2',
  passwd= 'pscale_pw_pEiVDtydTJqIpuJ68NRKenF0ncp6jjYipJkfxFDIHDN',
  db= 'js-lib-detect-trees',
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/cert.pem"   # For Mac
    #"ca": "/etc/ssl/certs/ca-certificates.crt"  # For Linux
  }
)

TABLE_NAME = 'DetectLib'

cursor = connection.cursor()
cursor.execute(f"SELECT libname, git FROM {TABLE_NAME};")
libnames = cursor.fetchall()

cnt = 0
for entry in libnames:
    libname = entry[0]
    raw_url = entry[1]
    
    star = 0

    if not raw_url:
      continue
    
    # Get star from Github API
    ptr = raw_url.find('github.com')
    if ptr == -1:
      continue

    # Remove ".git" suffix
    if raw_url[-4:] == '.git':
      raw_url = raw_url[:-4]
    github_api_url = f'https://api.github.com/repos{raw_url[ptr+10:]}'

    # try:
    req = Request(github_api_url)
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    repo_info = json.loads(urlopen(req).read())

    time.sleep(1) # Not to request too fast
    if repo_info['stargazers_count']:
      star = repo_info['stargazers_count']
    # except:
    #   print(f'404 error: {github_api_url}')
        
    sql = f"UPDATE {TABLE_NAME} SET star = %s WHERE libname = %s;"
    val = (star, libname)
    cursor.execute(sql, val)
    connection.commit()

    cnt += 1
    print(f'{cnt}: {libname} updated.')
    
connection.close()

# CREATE TABLE jslibs_lastest (
# 	name VARCHAR(255) NOT NULL,
# 	version VARCHAR(255),
# 	file_num INT,
# 	file_list JSON, 
#   PRIMARY KEY (name)
# );