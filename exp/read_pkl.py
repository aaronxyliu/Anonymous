from urllib.request import urlopen
import json
import pickle


# open a file, where you stored the pickled data
file = open('data/crawler4_res.pkl', 'rb')

# dump information to that file
data = pickle.load(file)

# close the file
file.close()

print(data)
