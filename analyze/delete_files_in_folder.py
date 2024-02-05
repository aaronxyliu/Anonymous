def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Remove newline characters from each line
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []

# Example usage:
file_path = 'log/css_libs.log'  # Replace with your actual file path
files_to_delete = read_file_lines(file_path)


import os

def delete_files_in_folder(folder_path, files_to_delete):
    try:
        for file_name in files_to_delete:
            file_path = os.path.join(folder_path, file_name) + '.json'
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_name}")
            else:
                print(f"File not found: {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
folder_path = 'static/libs_data'  # Replace with your actual folder path
delete_files_in_folder(folder_path, files_to_delete)
