import os
import sys

# Example usage "python rename.py ../../image00.h5.h5 image00"

def rename_file(file_path, new_name):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Get the directory where the file is located
    directory = os.path.dirname(file_path)

    # Get the original filename without the path
    original_filename = os.path.basename(file_path)

    # Get the file extension
    file_extension = os.path.splitext(original_filename)[1]

    # Construct the new name by using the provided name and the original extension
    new_file_name = f"{new_name}{file_extension}"

    # Rename the file
    try:
        os.rename(file_path, os.path.join(directory, new_file_name))
        print(f"Renamed '{original_filename}' to '{new_file_name}'")
    except Exception as e:
        print(f"Error renaming '{original_filename}': {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rename_file.py <file_path> <new_name> WITHOUT EXTENSION (e.g., image00)")
    else:
        file_path = sys.argv[1]
        new_name = sys.argv[2]
        rename_file(file_path, new_name)
