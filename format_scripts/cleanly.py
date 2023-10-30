import sys
import os

def format_output(output_file_path, drop_questionable_rows):
    if not output_file_path.endswith(".txt"):
        return 0  # Return 0 if the file is not a .txt file

    with open(output_file_path, 'r') as f:
        lines = f.readlines()

    num_question_marks = 0

    formatted_lines = []
    header_row = "         h          k          l       FREE         FP      SIGFP         FC       PHIC     FC_ALL   PHIC_ALL        FWT       PHWT     DELFWT    PHDELWT        FOM  FC_ALL_LS PHIC_ALL_LS"

    for line in lines[1:]:
        # Check if the line contains a question mark
        if "?" in line:
            if drop_questionable_rows:
                continue  # Skip the line if it contains a question mark and drop_questionable_rows is True
            else:
                num_question_marks += line.count("?")  # Count the number of "?" in the line
        else:
            num_question_marks += line.count("?")  # Count the number of "?" in the line

        # Split the line into columns
        columns = line.split()

        # Format the columns (excluding the first column)
        formatted_columns = []
        for column in columns[1:]:
            formatted_column = '{:>10}'.format(column)
            formatted_columns.append(formatted_column)

        # Join the formatted columns into a single line
        formatted_line = ' '.join(formatted_columns)

        # Add the formatted line to the list of formatted lines
        formatted_lines.append(formatted_line)

    formatted_lines.insert(0, header_row)

    # Write the formatted text to a new file
    output_file_name = os.path.basename(output_file_path)
    output_file_name = os.path.splitext(output_file_name)[0] + "_formatted.txt"
    with open(output_file_name, 'w') as f:
        f.write('\n'.join(formatted_lines))

    return num_question_marks

def format_input(input_file_path, drop_questionable_rows):
    if not input_file_path.endswith("_input.txt"):
        return 0  # Return 0 if the file is not an input file

    with open(input_file_path, 'r') as f:
        lines = f.readlines()

    num_question_marks = 0

    formatted_lines = []
    header_row = "         h          k          l       FREE         FP      SIGFP         FC       PHIC     FC_ALL   PHIC_ALL        FWT       PHWT     DELFWT    PHDELWT        FOM  FC_ALL_LS PHIC_ALL_LS"

    for line in lines[1:]:
        # Check if the line contains a question mark
        if "?" in line:
            if drop_questionable_rows:
                continue  # Skip the line if it contains a question mark and drop_questionable_rows is True
            else:
                num_question_marks += line.count("?")  # Count the number of "?" in the line
        else:
            num_question_marks += line.count("?")  # Count the number of "?" in the line

        # Split the line into columns
        columns = line.split()

        # Format the columns (excluding the first column)
        formatted_columns = []
        for column in columns[1:]:
            formatted_column = '{:>10}'.format(column)
            formatted_columns.append(formatted_column)

        # Join the formatted columns into a single line
        formatted_line = ' '.join(formatted_columns)

        # Add the formatted line to the list of formatted lines
        formatted_lines.append(formatted_line)

    formatted_lines.insert(0, header_row)
    
    # Write the formatted text to a new file
    output_file_name = os.path.basename(input_file_path)
    output_file_name = os.path.splitext(output_file_name)[0] + "_formatted.txt"
    with open(output_file_name, 'w') as f:
        f.write('\n'.join(formatted_lines))
    return num_question_marks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py file1_input.txt file2_input.txt ... file1_output.txt file2_output.txt ...")
        sys.exit(1)

    input_files = []
    output_files = []

    for arg in sys.argv[1:]:
        if arg.endswith("_input.txt"):
            input_files.append(arg)
        elif arg.endswith("_output.txt"):
            output_files.append(arg)
        else:
            print(f"Skipping {arg} - not an input or output file")

    total_question_marks = 0

    for input_file in input_files:
        num_question_marks = format_input(input_file, False)  # Set to True if you want to drop rows with question marks
        total_question_marks += num_question_marks
        print(f"{input_file}: type INPUT")
        print(f"{input_file}: {num_question_marks} question marks")
        
    for output_file in output_files:
        num_question_marks = format_output(output_file, False)  # Set to True if you want to drop rows with question marks
        total_question_marks += num_question_marks
        print(f"{output_file}: type OUTPUT")
    print(f"Total question marks in all files: {total_question_marks}")

    drop_rows_response = input("Would you like to drop rows with question marks (yes/no)? ")
    if drop_rows_response.lower() == 'yes':
        input_files = []
        output_files = []
        for arg in sys.argv[1:]:
            if arg.endswith("_input.txt"):
                input_files.append(arg)
            elif arg.endswith("_output.txt"):
                output_files.append(arg)

        total_question_marks = 0

        for input_file in input_files:
            num_question_marks = format_input(input_file, True)  # Set to True to drop rows with question marks
            total_question_marks += num_question_marks
            print(f"{input_file}: type INPUT (after dropping rows with question marks)")
            print(f"{input_file}: {num_question_marks} question marks removed")
            
        for output_file in output_files:
            num_question_marks = format_output(output_file, True)  # Set to True to drop rows with question marks
            total_question_marks += num_question_marks
            print(f"{output_file}: type OUTPUT (after dropping rows with question marks)")
            print(f"{output_file}: {num_question_marks} question marks removed")
        print(f"Total question marks in all files (after dropping rows with question marks): {total_question_marks}")
