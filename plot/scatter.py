import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

df= pd.read_csv("./plot/time.csv")
y_ = df['T'].tolist()
x_ = df['n|V|'].tolist()
k = 1 / 300000

x = np.arange(0, 50000000, 100000)
y = []
for t in x:
    y_1 = k * t
    y.append(y_1)
plt.plot(x, y, label="Time = n ⋅ N / 300000", linestyle='--', color='#1c4586')
plt.xlabel("n ⋅ N")
plt.ylabel("Time (sec)")
# y2 = []
# for t in x:
#     y_1 = k * t * t
#     y2.append(y_1)
# plt.plot(x, y2, label="y=x2")

plt.scatter(x_, y_)
plt.legend()
plt.show()