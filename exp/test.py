import pandas as pd 
# List1 
lst = [['apple', 'red', 11], ['grape', 'green', 22], ['orange', 'orange', 33], ['mango', 'yellow', 44]] 
df = pd.DataFrame(lst, columns =['Fruits', 'Color', 'Value'], dtype = float) 
print(df)