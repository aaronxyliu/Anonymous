# Minify pTree size for each version

from tree import *
import json
import pandas as pd
from database_conn import connect_to_localdb
import time
import sys
import os


# corejs: 21.43 s
# requirejs: 1.52 s
# momentjs: 5.15 s
# jqueryui: 1.5 s


connection = connect_to_localdb()
cursor = connection.cursor()


def Json2LT(root, par_v=None):
    '''
    Convert JSON object to the labeled tree data structure defined in tree.py

    Parameters:
        root - the root of the JSON tree
        par_v - parent vertex in "Vertex" type

    Output:
        root of the new tree in "Vertex" type
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

def print_S(G):
    assert(isinstance(G, Gamma))
    print("\n== Supertree Set Display ==\n")
    for i in range(len(G.trees)):
        print(G.trees[i].name + ':')
        print("    " + str(G.trees[i].S))


def minify_pTs(libname):

    INPUT_TABLE = f'{libname}_version'
    OUTPUT_TABLE = f'{libname}_version_m2'


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
        # if entry[1] == '4.16.5' or entry[1] == '4.16.6':
        #     pTree = Json2LT(json.loads(entry[0]))
        #     G.addt(LabeledTree(pTree, str(entry[1])))

    T1 = time.time()    # Timer starts

    # Minification
    t1 = G.get_equivalence()
    G.get_trees_metas()

    print('Get equivalence finished.')

    t2 = G.tree_size_reduction()
    G.get_mtrees_metas()

    print('Tree size reduction finished.')

    # print_S(G)

    t3 = G.strict_supertree_set_minify()
    T2 = time.time()    # Timer ends

    print('Strict supertree set minification finished.')

    # Drop table if exists
    cursor.execute(f'DROP TABLE IF EXISTS `{OUTPUT_TABLE}`;')
    connection.commit()

    # Create a new output table
    cursor.execute(f'''CREATE TABLE `{OUTPUT_TABLE}` (
        `pTree` json DEFAULT NULL,
        `size` int DEFAULT NULL,
        `depth` int DEFAULT NULL,
        `version` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
        `file_id` int DEFAULT NULL,
        `Sm` json DEFAULT NULL,
        `version_list` json DEFAULT NULL
        );''')
    connection.commit()
    print(f'Create table {OUTPUT_TABLE} to store minified pTrees.')

    # Save minified pTrees to dataset
    for i in range(len(G.trees)):
        assert(len(G.trees) == len(G.mtrees))
        mTree = G.mtrees[i].root
        version = G.mtrees[i].name
        Sm = G.trees[i].Sm
        version_list = G.trees[i].eq_name_list

        mTree = LT2Json(mTree)

        sql = f'''INSERT INTO `{OUTPUT_TABLE}` 
                (pTree, size, depth, version, file_id, Sm, version_list) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        val = (json.dumps(mTree), G.mtrees[i].size, G.mtrees[i].depth, version, i, json.dumps(list(Sm)), json.dumps(version_list))
        cursor.execute(sql, val)
        connection.commit()
        print(f'   Version {version} entry added to {OUTPUT_TABLE}.')
    
    print(f'Tree minification completed. Time spent: {(T2 - T1)} seconds.')
    return t1 + t2 + t3 + [T2 - T1]


def minifyAll():
    # Iterate through all libraries with information under the static/libs_data folder
    libfiles_list = os.listdir('static/libs_data')
    libfiles_list.sort()

    log = []
    for fname in libfiles_list:
        
        libname = fname[:-5]
        res = minify_pTs(libname)
        if res:
            log.append([libname] + res)

    df = pd.DataFrame(log, columns =['Library', 'Equivalence', 'Color Set', 'Supertree Set', 'Min Cover Set', 'Get mT', 'Get Sm', 'Total']) 
    df.to_csv(f'log/mini_pTs2.csv', index=True)

if __name__ == '__main__':
    # Usage: > python3 mini_pTs.py <lib name>

    if len(sys.argv) > 1:
        minify_pTs(sys.argv[1])
    else:
        minifyAll()
    connection.close()