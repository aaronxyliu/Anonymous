# Crawl all jQuery files under each version

from urllib.request import urlopen
import json
import pandas as pd


FILE_NAME = 'data/Libraries.csv'
df = pd.read_csv(FILE_NAME)
for i in range(df.shape[0]):
    CDN_url = df.loc[i, 'CDNJS']
    if CDN_url == 'None' or not CDN_url:
        continue

    libname= CDN_url[CDN_url.rfind('/')+1:]
    res = urlopen(f'https://api.cdnjs.com/libraries/{libname}')
    lib_info = json.loads(res.read())

    file_list = []
    for version in lib_info['versions']:
        res2 = urlopen(f'https://api.cdnjs.com/libraries/{libname}/{version}')
        v_info = json.loads(res2.read())
        file_list.append({
            'version': version,
            'files': v_info['files']
        })

        # print(f"{version}:    {str(v_info['files'])}")

    save_path = f'data/lib_versions/{libname}_v.json'
    with open(save_path, "w") as outfile:
        outfile.write(json.dumps(file_list))

    print(f'{libname} version information results are saved to {save_path}')