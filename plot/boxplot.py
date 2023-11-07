
# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
 
 
# df= pd.read_csv("./plot/fineness.csv")
df= pd.read_csv("./plot/None.csv")

size_list = df['PTV Fineness'].tolist()
size_list2 = df['LDC Fineness'].tolist()


# Init a figure and axes
fig, ax = plt.subplots(figsize=(3.2, 2.8))

# Create the plot with different colors for each group
boxplot = ax.boxplot(x=[size_list, size_list2],
                     labels=['Fineness of PTV', 'Fineness of LDC'],
                     patch_artist=True,
                     medianprops={'color': 'black'},
                     widths=0.35
                    ) 

# Define colors for each group
colors = ["#F5CCCC", "#9FC5E9"]

# Assign colors to each box in the boxplot
for box, color in zip(boxplot['boxes'], colors):
    box.set_facecolor(color)


# Display it
plt.show()