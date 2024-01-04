import argparse
import json
import re

def add_deps(libname, dep, index_set):
    with open(f'static/libs_data/{libname}.json', "r") as infile:
        file_dict = json.load(infile)
    
    if len(index_set) == 0:
        for version_info in file_dict.items():
            version_info[1]['in_deps'].append(str(dep))
    else:
        for index in index_set:
            file_dict[index]['in_deps'].append(str(dep))
    
    with open(f'static/libs_data/{libname}.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='add_indeps.py',
                    description='Add inner dependecy to the library files in `static` folder. One dependecy each time.')
    parser.add_argument('range_strs', metavar='R', type=str, nargs='*', 
                    help='''A range string. Corresponeding to the 'file_id' field in the database.
                            A prefix 'm' means discarding the following range.
                            The symbol '~' means range from one value to another value.
                            For example, <1 2 4~7 m5> refers to the array [1, 2, 4, 6, 7].''')
    parser.add_argument('--library', '-l', metavar='<lib>', help='the library name (required)', required=True)
    parser.add_argument('--dep', '-d', metavar='<dep>', help='dependency url (required)', required=True)
    args = parser.parse_args()

    index_set = set()
    for range_str in args.range_strs:
        if re.match('m?[0-9]+$', range_str):
            # single
            if range_str[0] == 'm':
                index_set.discard(int(range_str[1:]))
            else:
                index_set.add(int(range_str))
        elif re.match('m?[0-9]+~[0-9]+$', range_str):
            # mutiple
            loc = range_str.find('~')
            if range_str[0] == 'm':
                start = int(range_str[1: loc])
                end = int(range_str[loc+1: ])
                for i in range(start, end + 1):
                    index_set.discard(i)
            else:
                start = int(range_str[0: loc])
                end = int(range_str[loc+1: ])
                for i in range(start, end + 1):
                    index_set.add(i)
        else:
            print(f'Invalid argument: {range_str}')
            exit(0)
    add_deps(args.library, args.dep, index_set)