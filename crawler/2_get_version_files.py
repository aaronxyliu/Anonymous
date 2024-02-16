# Crawl all version files from Cdnjs, and select the main file, store in the `static/libs_data` folder

from urllib.request import urlopen
import json
import ultraimport
logger = ultraimport('__dir__/../utils/logger.py').getLogger()
conn = ultraimport('__dir__/../utils/sqlHelper.py').ConnDatabase('Libraries')

# Github API rate limit: 5000/hr
# Token generation: https://github.com/settings/tokens
LIBRARY_TABLE = 'libs_cdnjs'

EXTRA_BONUS = 200  # the credit bonus for the file name which is similar to the library name


def select_file_for_each_version(files, patten_dict):
    # Return a single file path for each version
    for pattern in patten_dict:
        for filepath in files:
            if valid_webjs(filepath):
                filename = filepath[filepath.rfind('/') + 1 :]
                filename_body = filename[: filename.find('.')].lower()
                if filename_body == pattern:
                    return filepath
    return None


def get_file_list_from_cdnjs(libname):
    file_list = []
    lib_url = f'https://api.cdnjs.com/libraries/{libname}'
    try:
        res = urlopen(lib_url)
    except KeyboardInterrupt:
        pass
    except:
        logger.error(f'[HTTP Error] {lib_url}')
        return file_list
    
    lib_info = json.loads(res.read())
    logger.info(f"{len(lib_info['versions'])} versions of {libname} found.")
    for version in lib_info['versions']:
        if version[0] == '%':
            # %npm_package_version%
            continue
        logger.info(version)
        version_url = f'https://api.cdnjs.com/libraries/{libname}/{version}'
        try:
            res2 = urlopen(version_url)
        except KeyboardInterrupt:
            pass
        except:
            logger.error(f'[HTTP Error] {version_url}')
            continue
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

def freq_filename_pattern(file_list, libname):
    pattern_freq_dict = {}
    for item in file_list:
        files = item['jsfiles']
        pattern_set = set()     # Use set to prevent one pattern counts mutiple times in one version
        for filepath in files:
            if valid_webjs(filepath):
                filename = filepath[filepath.rfind('/') + 1 :]
                filename_body = filename[: filename.find('.')].lower()
                pattern_set.add(filename_body)
        
        for pattern in pattern_set:
            if pattern not in pattern_freq_dict:
                pattern_freq_dict[pattern] = 1
            else:
                pattern_freq_dict[pattern] += 1

    # Add bonus if the pattern is similar to the library name
    for pattern in pattern_freq_dict:
        if isSimilar(pattern, libname):
            pattern_freq_dict[pattern] += EXTRA_BONUS

    # Sort by frequency from large to small
    sorted_dict = dict(sorted(pattern_freq_dict.items(), key=lambda x:x[1], reverse=True))
    return sorted_dict

def isSimilar(s1, s2):
    # Check whehter two strings are similar
    if len(s1) > 4 and len(s2) > 4:
        s1 = s1.lower()
        s2 = s2.lower()
        if isSubsequence(s1, s2) or isSubsequence(s2, s1):
            return True
    return False

def isSubsequence(s: str, t: str) -> bool:
    # Check whether s is a sub sequence of t
    s_len = len(s)
    t_len = len(t)

    # Define two pointers linking to the original locations of s and t
    p = 0
    q = 0

    while p < s_len and q < t_len:
        # When the characters match
        # move p and q simutaneously
        if s[p] == t[q]:
            p += 1
        # If there is no match, only the q-pointer is moved, and the character corresponding to the p-pointer continues to be matched.
        q += 1
    # Return True if the p pointer reaches the end of s.
    return p == s_len


def valid_webjs(filepath):
    filepath = filepath.lower()
    invalid_patterns = ['amd/', 'esm/', 'es6/', 'cjs/', '/amd', '/esm', '/es6', '/cjs', 'amd.', 'esm.', 'es6.', 'cjs.', '.amd', '.esm', '.es6', '.cjs']
    for pattern in invalid_patterns:
        if pattern in filepath:
            return False
    return True


res = conn.fetchall(f"SELECT `libname`, `#versions`, `github` FROM `{LIBRARY_TABLE}` ORDER BY `star` DESC;")

libcnt = 1
# start = False

github_url_set = set()

for entry in res:
    if libcnt > 1000 - 94 -79 -206:
        break

    libname = entry[0]
    version_num = entry[1]
    github = entry[2]

    if version_num > 200:
        continue
    
    # if libname == 'javascript-state-machine':
    #     start = True
    # if not start:
    #     continue
    

    # Prevent counting repeated github repo 
    if github and github in github_url_set:
        libcnt -= 1
    github_url_set.add(github)
    
    file_list = get_file_list_from_cdnjs(libname)
    pattern_dict = freq_filename_pattern(file_list, libname)
    logger.info(pattern_dict)

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

            logger.warning(f'No matched file found: {libname}: {version}')
        cnt += 1
    
    with open(f'static/libs_data/{libname}.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

    logger.info(f'{libcnt} {libname} results saved.')

    libcnt += 1

conn.close()
logger.close()



    
            
   


    

    
