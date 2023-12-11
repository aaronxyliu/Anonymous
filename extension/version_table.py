# Convert mpT table for each version from database to json file

import MySQLdb
import sys
import json

def connect_to_localdb():
    connection = MySQLdb.connect(
        host= '127.0.0.1',
        user='root',
        passwd= '12345678',
        db= 'Library Version pTrees',
        autocommit = True
    )
    return connection

connection = connect_to_localdb()
cursor = connection.cursor()

def convert(libname, start_id=None, end_id=None):
    INPUT_TABLE = f'{libname}_version_m2'

    # Check wehther the table exist
    query = f'''SELECT pTree, version, file_id, Sm, version_list FROM `{INPUT_TABLE}`'''
    cursor.execute(query)
    res = cursor.fetchall()

    if start_id == None:
        start_id = str(res[0][2])
    if end_id == None:
        end_id = str(res[len(res) - 1][2])

    # Read pTrees from dataset
    output_json = {}
    valid_version = False
    for entry in res:
        tree_id = str(entry[2])
        if tree_id == start_id:
            valid_version = True
        
        if valid_version:
            output_json[entry[2]] = {
                'pTree': json.loads(entry[0]),
                'version': str(entry[1]),
                'Sm': json.loads(entry[3]),
                'version_list': json.loads(entry[4])
            }        
        
        if tree_id == end_id:
            valid_version = False

    with open(f'extension/output/{libname}.json', 'w') as f:
       json.dump(output_json, f)


if __name__ == '__main__':
    # Usage: > python3 extension/version_table.py <lib name> <start id> <end id>

    if len(sys.argv) == 2:
        convert(sys.argv[1])
    elif len(sys.argv) == 3:
        convert(sys.argv[1], str(sys.argv[2]))
    elif len(sys.argv) == 4:
        convert(sys.argv[1], str(sys.argv[2]), str(sys.argv[3]))
    connection.close()