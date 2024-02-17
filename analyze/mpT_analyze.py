
import pandas as pd
from database_conn import connect_to_localdb
import time
import sys
import os

connection = connect_to_localdb()
cursor = connection.cursor()

FILE_NAME = 'data/Libraries.csv'
df = pd.read_csv(FILE_NAME)
for i in range(df.shape[0]):
    CDN_url = df.loc[i, 'CDNJS']
    libname = CDN_url[CDN_url.rfind('/')+1:]
    table_name = f'{libname}_version'
    m_table_name = f'{libname}_version_m'

    # Check wehther the table exist
    cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{m_table_name}'")
    if cursor.fetchone()[0] != 1:
        continue

    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
    version_num = cursor.fetchone()[0]

    cursor.execute(f"SELECT COUNT(*) FROM `{m_table_name}`")
    m_version_num = cursor.fetchone()[0]

    df.loc[i, '# Versions'] = version_num
    df.loc[i, '# Sep by PT'] = m_version_num
    df.loc[i, 'Fineness'] = round(m_version_num / version_num, 2)

df.to_csv(FILE_NAME, index=False)

    