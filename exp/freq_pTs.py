# Find the maximum frequrent subtree

from tree import *
import json
import pandas as pd
from database_conn import connect_to_localdb
import time
import sys
import os

connection = connect_to_localdb()
cursor = connection.cursor()

OUTPUT_TABLE = 'max_freq_subtree'


def Json2LT(root, par_v=None):
    '''
    Convert JSON object to the labeled tree data structure defined in tree.py

    Parameters:
        root - the root of the JSON tree
        par_v - parent vertex in "Vertex" type

    Output:
        root of the new tree in "Vertex"
    '''
    if not root:
        return None
    v = Vertex(root['n'], root['d'])
    if par_v:
        par_v.addc(v)
    for child in root['c']:
        Json2LT(child, v)
    return v


def LT2Json(root, par_v=None):
    '''
    Convert the labeled tree back to JSON object

    Parameters:
        root - the root of the labeled tree
        par_v - parent vertex in JSON object type

    Output:
        root of the new tree in JSON object type
    '''
    if not root:
        return None
    assert(isinstance(root, Vertex))
    v_obj = {
        'n': root.name,
        'd': root.label,
        'c':[]
    }
    if par_v:
        par_v['c'].append(v_obj)
    for child in root.children:
        LT2Json(child, v_obj)
    return v_obj


def freq_pTs(libname):
    INPUT_TABLE = f'{libname}_version'


    # Check wehther the table exist
    query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{INPUT_TABLE}'"
    cursor.execute(query)
    if cursor.fetchone()[0] != 1:
        print(f'Library {libname} doesn\'t have pTrees information stored in the database. Skipped.')
        return None

    G = Gamma()
    cursor.execute(f"SELECT `pTree`, `version` FROM `{INPUT_TABLE}`;")
    res = cursor.fetchall()

    # Read pTrees from dataset
    for entry in res:
        pTree = Json2LT(json.loads(entry[0]))
        G.addt(LabeledTree(pTree, str(entry[1])))

    # Generate the maximun frequent subtree
    freqT = G.max_freq_subtree()
    freqT.get_metas()

    # Save to dataset
    sql = f'''INSERT INTO `{OUTPUT_TABLE}` 
            (pTree, size, depth, libname) 
            VALUES (%s, %s, %s, %s);'''
    val = (json.dumps(LT2Json(freqT.root)), freqT.size, freqT.depth,libname)
    cursor.execute(sql, val)
    connection.commit()
    print(f'   Library {libname} entry added to {OUTPUT_TABLE}.')
    


def freqAll():
    

    # Drop table if exists
    cursor.execute(f'DROP TABLE IF EXISTS `{OUTPUT_TABLE}`;')
    connection.commit()

    # Create a new output table
    cursor.execute(f'''CREATE TABLE `{OUTPUT_TABLE}` (
        `pTree` json DEFAULT NULL,
        `size` int DEFAULT NULL,
        `depth` int DEFAULT NULL,
        `libname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
        );''')
    connection.commit()
    print(f'Create table {OUTPUT_TABLE} to store maximun frequent subtrees.')

    # Iterate through all libraries with information under the static/libs_data folder
    libfiles_list = os.listdir('static/libs_data')
    libfiles_list.sort()

    for fname in libfiles_list:
        libname = fname[:-5]
        freq_pTs(libname)
        

if __name__ == '__main__':
    # Usage: > python3 mini_pTs.py <lib name>

    if len(sys.argv) > 1:
        freq_pTs(sys.argv[1])
    else:
        freqAll()
    connection.close()