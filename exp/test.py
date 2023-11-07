import pandas as pd

log = [[1,3,5]]
df = pd.DataFrame(log, columns =['Version', 'Success', 'Description']) 
df.to_csv(f'log/mini_pTs.csv', index=True)