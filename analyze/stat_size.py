# Get pTree size statistics for each library version

from database_conn import connect_to_localdb
import pandas as pd


connection = connect_to_localdb()
cursor = connection.cursor()

FILE_NAME = 'data/TargetLibs.csv'

SUM_SIZE = 0
VERSION_NUM = 0
SUM_SIZE_M = 0
SEP_NUM = 0

df = pd.read_csv(FILE_NAME)
for i in range(df.shape[0]):
    CDN_url = df.loc[i, 'CDNJS']
    if CDN_url == 'None' or not CDN_url:
        continue
    libname= CDN_url[CDN_url.rfind('/')+1:]

    cursor.execute(f"SELECT SUM(size) FROM `{libname}_version`;")
    res = cursor.fetchone()
    sum_size = res[0]
    SUM_SIZE += sum_size

    cursor.execute(f"SELECT COUNT(*) FROM `{libname}_version`;")
    res = cursor.fetchone()
    version_num = res[0]
    VERSION_NUM += version_num

    cursor.execute(f"SELECT SUM(size) FROM `{libname}_version_m`;")
    res = cursor.fetchone()
    sum_size_m = res[0]
    SUM_SIZE_M += sum_size_m

    cursor.execute(f"SELECT COUNT(*) FROM `{libname}_version_m`;")
    res = cursor.fetchone()
    sep_num = res[0]
    SEP_NUM += sep_num

    df.loc[i, '# Versions'] = version_num
    df.loc[i, '# Sep by PT'] = sep_num
    df.loc[i, '|V|'] = sum_size
    df.loc[i, 'avg. |V|'] = round(sum_size /  version_num, 1)
    df.loc[i, 'avg. |Vm|'] = round(sum_size_m /  sep_num, 1)

print(f'Total size: {SUM_SIZE}    Total size minized: {SUM_SIZE_M}')
print(f'Total average size: {round(SUM_SIZE / VERSION_NUM, 1)}')
print(f'Total average size after minification: {round(SUM_SIZE_M / SEP_NUM, 1)}')

df.to_csv(FILE_NAME, index=False)

