# Get the distribution of F(PT)/F(LDC)
import pandas as pd


FILE_NAME = 'data/TargetLibs.csv'

dist_range = [(0, 1), (1, 1.25), (1.25, 1.75), (1.75, 2.75), (2.75, 4.75), (4.75, 8.75), (8.75, 16.75), (16.75, 200)]
dist_num = [0] * len(dist_range)

df = pd.read_csv(FILE_NAME)
for i in range(df.shape[0]):
    ff = df.loc[i, 'F(PT)/F(LDC)']
    for i in range(len(dist_range)):
        _range = dist_range[i]
        if ff > _range[0] and ff <= _range[1]:
            dist_num[i] += 1
    if ff > 4:
        print(ff)


    
    
print(dist_num)
