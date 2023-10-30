import argparse
import glob
import os

def extract_crystal_names(file_names):
    crystal_names = []
    for file_name in file_names:
        if '.' in file_name:
             # Split the path by '/' and get the last part
            parts = file_name.split('/')
            crystal_name = parts[-1]
            crystal_name, _ = os.path.splitext(crystal_name)
            crystal_names.append(file_name.split('.')[0])
        elif '_' in file_name:
            parts = file_name.split('/')
            crystal_name = parts[-1]
            crystal_name, _ = os.path.splitext(crystal_name)
            crystal_names.append(file_name.split('_')[0])
    return crystal_names


def extract_crystal_names(file_paths):
    crystal_names = []
    for file_path in file_paths:
        # Split the path by '/' and get the last part
        parts = file_path.split('/')
        crystal_name = parts[-1]
        crystal_names.append(crystal_name)
    return crystal_names



def main():
    parser = argparse.ArgumentParser(description="Extract crystal names from file names")
    parser.add_argument("file_patterns", nargs='+', help="File patterns to extract crystal names (e.g., *.txt)")

    args = parser.parse_args()

    file_names = []
    for pattern in args.file_patterns:
        matching_files = glob.glob(pattern)
        file_names.extend(matching_files)

    if not file_names:
        print("No matching files found.")
        return

    # Extract crystal names
    crystal_names = extract_crystal_names(file_names)

    # Print the extracted crystal names
    for name in crystal_names:
        print(name)

if __name__ == "__main__":
    main()
