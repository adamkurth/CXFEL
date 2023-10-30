import sys

def remove_first_column_from_files(files):
    for file_path in files:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Process the lines, removing the first column
            processed_lines = [line.split(None, 1)[1] for line in lines]

            with open(file_path, 'w') as file:
                file.writelines(processed_lines)

            print(f"Processed '{file_path}' - removed first column.")
        except Exception as e:
            print(f"Error processing '{file_path}': {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_first_column.py file1.txt file2.txt ...")
    else:
        input_files = sys.argv[1:]
        remove_first_column_from_files(input_files)
