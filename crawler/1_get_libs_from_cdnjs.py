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

def get_star(lib_info):
    try:
        raw_url = lib_info['repository']['url']
    except:
        print(f'{libname} doesn\'t have repository information.')
        return 0

    # Get star from Github API
    ptr = raw_url.find('github.com')
    if ptr == -1:
        print('Not a github domain.')
        return 0

    # Remove ".git" suffix
    if raw_url[-4:] == '.git':
        raw_url = raw_url[:-4]
    github_api_url = f'https://api.github.com/repos{raw_url[ptr+10:]}'
    
    req = Request(github_api_url)
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    try:
        repo_info = json.loads(urlopen(req).read())
    except:
        print(f"{github_api_url} is an invalid url. Or github token is outdated.")
        return 0
    
    if repo_info['stargazers_count']:
        star = repo_info['stargazers_count']
        return int(star)
    else:
        print('Failed to find the stargazers field.')
        return 0

res = urlopen(f'https://api.cdnjs.com/libraries')
lib_list = json.loads(res.read())['results']
lib_num = len(lib_list)
cnt = 0

for lib_entry in lib_list:
    cnt += 1
    if cnt <= 3879:
        continue
    libname = lib_entry['name']
    cdnjs = f'https://cdnjs.com/libraries/{libname}'
    res = urlopen(f'https://api.cdnjs.com/libraries/{libname}')
    lib_info = json.loads(res.read())
    url = lib_info['homepage'] if 'homepage' in lib_info else None
    dscp = lib_info['description'] if 'description' in lib_info else None
    version_list = lib_info['versions']
    version_num = 0
    latest_version = None
    if version_list and len(version_list) > 1:
        version_num = len(lib_info['versions'])
        latest_version = lib_info['versions'][-1]
    star = get_star(lib_info)    
    sql = f'''INSERT INTO `{OUTPUT_TABLE}` 
            (libname, url, cdnjs, star, description, `#versions`, `latest version`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);'''
    val = (libname, url, cdnjs, star, dscp, version_num, latest_version)
    cursor.execute(sql, val)
    connection.commit() 
    print(f'{libname} finished. ({cnt} / {lib_num})')
    time.sleep(0.5)
