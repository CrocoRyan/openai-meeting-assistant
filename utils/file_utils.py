import os

def create_folder_if_not_exist(file_path):
    # Extract the directory part of the file path
    folder_path = os.path.dirname(file_path)

    # Check if the directory exists
    if not os.path.exists(folder_path):
        # Create the directory
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

