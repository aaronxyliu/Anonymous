import csv
import os
import json

def filter_and_save_to_csv(list1, list2, output_csv_path):
    result_list = [item for item in list1 if item not in list2]

    try:
        with open(output_csv_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Filtered Elements'])
            csv_writer.writerows([[item] for item in result_list])
        print(f"Filtered elements saved to: {output_csv_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
lib_files = os.listdir('static/libs_data/')
input_list1 = [filename[: -5] for filename in lib_files]
# print(input_list1[0])
with open(f'extension/libraries.json', 'r') as openfile:
    libs = json.load(openfile)

input_list2 = [lib['libname'] for lib in libs]
# print(input_list2[0])

output_csv_path = 'data/dep_libs.csv'

filter_and_save_to_csv(input_list1, input_list2, output_csv_path)
