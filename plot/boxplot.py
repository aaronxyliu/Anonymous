
# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
 
 
# df= pd.read_csv("./plot/fineness.csv")
df= pd.read_csv("./plot/None.csv")

size_list = df['PTV Fineness'].tolist()
size_list2 = df['LDC Fineness'].tolist()

def boxplot_(list_data, list_data2):
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

def myboxplot(list_data, list_data2):


    # Create the plot with different colors for each group
    boxplot = plt.boxplot(x=[list_data, list_data2],
                        labels=['PTV', 'LDC'],
                        patch_artist=True,
                        medianprops={'color': 'black'},
                        widths=0.35
                        ) 

    # Define colors for each group
    colors = ["#F5CCCC", "#9FC5E9"]

    plt.ylabel('fineness')

    # Assign colors to each box in the boxplot
    for box, color in zip(boxplot['boxes'], colors):
        box.set_facecolor(color)


if __name__ == '__main__':
    plt.figure(figsize=(14,4))

    df= pd.read_csv("./plot/Full.csv")
    ptv_f = df['PTV Fineness'].tolist()
    ldc_f = df['LDC Fineness'].tolist()
    plt.subplot(1, 3, 1)
    myboxplot(ptv_f, ldc_f)

    df= pd.read_csv("./plot/Part.csv")
    ptv_f = df['PTV Fineness'].tolist()
    ldc_f = df['LDC Fineness'].tolist()
    plt.subplot(1, 3, 2)
    myboxplot(ptv_f, ldc_f)

    df= pd.read_csv("./plot/None.csv")
    ptv_f = df['PTV Fineness'].tolist()
    ldc_f = df['LDC Fineness'].tolist()
    plt.subplot(1, 3, 3)
    myboxplot(ptv_f, ldc_f)

    plt.show()