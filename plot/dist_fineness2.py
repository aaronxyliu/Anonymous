import pandas as pd
import math
import matplotlib.pyplot as plt

df= pd.read_csv("./plot/fineness.csv")
size_list = df['LDC Fineness'].tolist()
number_list = [0] * 6
for size in size_list:
    if size >= 0 and size < 0.2:
        number_list[0] += 1
    elif size >= 0.2 and size < 0.4:
        number_list[1] += 1
    elif size >= 0.4 and size < 0.6:
        number_list[2] += 1
    elif size >= 0.6 and size < 0.8:
        number_list[3] += 1
    elif size >= 0.8 and size < 1:
        number_list[4] += 1
    elif size == 1:
        number_list[5] += 1
    else:
        print(size)

print(number_list)
plt.bar(x=range(6), height=number_list, width=0.6,
       color="#9FC5E9",
        edgecolor="#1c4586")

# label_list = ["[0,0.2)", "[0.2,0.4)", "[0.4,0.6)", "[0.6,0.8)", "[0.8,1)", "1"]
label_list = ["0~.2", ".2~.4", ".4~.6", ".6~.8", ".8~1", "1"]
plt.xticks(range(6), label_list)
plt.xlabel("Fineness of LDC")
plt.ylabel("Number")

plt.rcParams['figure.figsize'] = [2.5, 3]
plt.show()