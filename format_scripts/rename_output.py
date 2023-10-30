import os
import sys

def rename_files(directory):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # List files matching the pattern "*_hkl_out_formatted.txt"
    files_to_rename = [file for file in os.listdir(directory) if file.endswith("_hkl_out_formatted.txt")]
    
    if not files_to_rename:
        print(f"No matching files found in '{directory}'.")
        return
    
    for filename in files_to_rename:
        # Construct the new name by replacing "_hkl_out_formatted.txt" with "_output_formatted.txt"
        new_filename = filename.replace("_hkl_out_formatted.txt", "_output_formatted.txt")
        file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_filename)
        
        # Rename the file
        try:
            os.rename(file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")
        except Exception as e:
            print(f"Error renaming '{filename}': {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_files.py <directory>")
    else:
        directory = sys.argv[1]
        rename_files(directory)
