# Crawl all libraries and their Github star number from Cdnjs

from urllib.request import Request, urlopen
import json
import pandas as pd
import time
import MySQLdb

# Github API rate limit: 5000/hr
# Token generation: https://github.com/settings/tokens
LIBRARY_TABLE = 'libs_cdnjs'

connection = MySQLdb.connect(
    host= '127.0.0.1',
    user='root',
    passwd= '12345678',
    db= 'Libraries',
    autocommit = True
)
cursor = connection.cursor()



# Reset log content
with open(f'data/get_version_files.log', "w") as outfile:
    outfile.write('')

def select_file_for_each_version(files, patten_dict):
    # Return a single file path for each version
    for pattern in patten_dict:
        for filepath in files:
            filename = filepath[filepath.rfind('/') + 1 :]
            filename_body = filename[: filename.find('.')].lower()
            if filename_body == pattern:
                return filepath
    return None


def get_file_list_from_cdnjs(libname):
    file_list = []
    res = urlopen(f'https://api.cdnjs.com/libraries/{libname}')
    lib_info = json.loads(res.read())
    print(f"{len(lib_info['versions'])} versions of {libname} found.")
    for version in lib_info['versions']:
        if version[0] == '%':
            # %npm_package_version%
            continue
        print(version)
        res2 = urlopen(f'https://api.cdnjs.com/libraries/{libname}/{version}')
        files = json.loads(res2.read())['files']
        version_store_item = {
            'version': version,
            'jsfiles': []
        }
        for filepath in files:
            if len(filepath) >=4 and filepath[-2:] == 'js':
                version_store_item['jsfiles'].append(filepath)
        file_list.append(version_store_item)
    return file_list

def freq_filename_pattern(file_list):
    pattern_freq_dict = {}
    for item in file_list:
        files = item['jsfiles']
        pattern_set = set()     # Use set to prevent one pattern counts mutiple times in one version
        for filepath in files:
            filename = filepath[filepath.rfind('/') + 1 :]
            filename_body = filename[: filename.find('.')].lower()
            pattern_set.add(filename_body)
        
        for pattern in pattern_set:
            if pattern not in pattern_freq_dict:
                pattern_freq_dict[pattern] = 1
            else:
                pattern_freq_dict[pattern] += 1

    # Sort by frequency from large to small
    sorted_dict = dict(sorted(pattern_freq_dict.items(), key=lambda x:x[1], reverse=True))
    return sorted_dict

cursor.execute(f"SELECT `libname`, `#versions` FROM `{LIBRARY_TABLE}`;")
res = cursor.fetchall()
libcnt = 1
start = False

for entry in res:
    libname = entry[0]
    version_num = entry[1]

    if libname == 'jquery-datetimepicker':
        start = True
    if not start:
        continue
    if version_num > 200:
        continue
    if libcnt > 100:
        break
    file_list = get_file_list_from_cdnjs(libname)
    pattern_dict = freq_filename_pattern(file_list)

    file_dict = {}
    cnt = 1
    for item in file_list:
        selected_file = select_file_for_each_version(item['jsfiles'], pattern_dict)
        version = item['version']
        if selected_file:
            file_dict[cnt] = {
                'libname': libname,
                'filename': selected_file,
                'url': f"https://cdnjs.cloudflare.com/ajax/libs/{libname}/{version}/{selected_file}",
                'version': version,
                'in_deps': [],
                'out_deps': [],
            }
        else:
            file_dict[cnt] = {
                'libname': libname,
                'filename': '',
                'url': '',
                'version': version,
                'in_deps': [],
                'out_deps': [],
            }
            with open(f'data/get_version_files.log', "a") as outfile:
                outfile.write(f'{libcnt} {libname}: {version}    {str(pattern_dict)}\n')
        cnt += 1
    
    with open(f'static/more_libs_data/{libname}.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

    print(f'{libcnt} {libname} results saved.')

    libcnt += 1


    
            
   


    

    
