import json

with open(f'extension/libraries.json', 'r') as openfile:
    lib_list = json.load(openfile)

def byLibname(elem):
    return elem["libname"].lower()

lib_list.sort(key=byLibname)


with open(f'extension/libraries.json', 'w') as f:
    json.dump(lib_list, f, indent=4)