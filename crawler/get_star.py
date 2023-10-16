# Crawl all jQuery files under each version

from urllib.request import Request, urlopen
import json
import pandas as pd
import time

# Github API rate limit: 5000/hr
# Token generation: https://github.com/settings/tokens
GITHUB_TOKEN = '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'

FILE_NAME = 'data/Libraries.csv'
df = pd.read_csv(FILE_NAME)
for i in range(df.shape[0]):
    CDN_url = df.loc[i, 'CDNJS']
    if CDN_url == 'None' or not CDN_url:
        continue
    libname= CDN_url[CDN_url.rfind('/')+1:]
    res = urlopen(f'https://api.cdnjs.com/libraries/{libname}')
    lib_info = json.loads(res.read())
    try:
        raw_url = lib_info['repository']['url']
    except:
        print(f'{libname} doesn\'t have repository information.')
        continue

    # Get star from Github API
    ptr = raw_url.find('github.com')
    if ptr == -1:
        continue

    # Remove ".git" suffix
    if raw_url[-4:] == '.git':
        raw_url = raw_url[:-4]
    github_api_url = f'https://api.github.com/repos{raw_url[ptr+10:]}'
    print(github_api_url)
    
    req = Request(github_api_url)
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    try:
        repo_info = json.loads(urlopen(req).read())
    except:
        print(f"{github_api_url} is an invalid url.")
        continue

    time.sleep(1) # Not to request too fast
    if repo_info['stargazers_count']:
        star = repo_info['stargazers_count']
        df.loc[i, 'Star'] = int(star)

df.to_csv(FILE_NAME, index=False)