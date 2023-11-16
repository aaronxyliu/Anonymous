# defining the libraries 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 


def cdf(list_data, list_data2):
    data = np.array(list_data)
    data2 = np.array(list_data2)

    # getting data of the histogram 
    count, bins_count = np.histogram(data, bins=100) 
    count2, bins_count2 = np.histogram(data2, bins=100) 

    # finding the PDF of the histogram using count values 
    pdf = count / sum(count) 
    pdf2 = count2 / sum(count2) 

    # using numpy np.cumsum to calculate the CDF 
    # We can also find using the PDF values by looping and adding 
    cdf1 = np.cumsum(pdf) 
    cdf2 = np.cumsum(pdf2) 

    # plotting PDF and CDF 
    plt.plot(bins_count[1:], cdf1, color="#C66667", label="PTV") 
    plt.plot(bins_count2[1:], cdf2, linestyle='--' , color="#1c4586", label="LDC") 
    plt.xlabel('fineness')
    plt.ylabel('percentage')
    plt.legend() 


if __name__ == '__main__':
    plt.figure(figsize=(4,4))

    df= pd.read_csv("./plot/fineness.csv")
    ptv_f = df['PTV Fineness'].tolist()
    ldc_f = df['LDC Fineness'].tolist()
    cdf(ptv_f, ldc_f)


    plt.show()
