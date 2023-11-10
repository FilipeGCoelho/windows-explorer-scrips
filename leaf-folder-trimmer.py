import os

def delete_empty_folders(directory):
    is_empty = True

    # If not empty, recursively check its subdirectories
    for subdirectory in os.listdir(directory):
        full_path = os.path.join(directory, subdirectory)
        if os.path.isdir(full_path):
            if not delete_empty_folders(full_path):
                is_empty = False

    # Check if the directory is empty and delete if true
    if is_empty and not os.listdir(directory):
        print(f"Deleting empty folder: {directory}")
        os.rmdir(directory)
        return True
    else:
        return False

def main():
    source_path = input("Enter the source folder path: ")
    
    # Check if the source path exists
    if not os.path.exists(source_path):
        print("The provided path does not exist. Please enter a valid path.")
        return
    
    # Start the process
    delete_empty_folders(source_path)

    print("Empty folders deletion complete.")

if __name__ == "__main__":
    main()
