import os
import argparse

def clean_file(input_file, output_file):
    # Open the input file for reading
    with open(input_file, "r") as f_in:
        # Read in the lines of the file
        lines = f_in.readlines()

    # Open the output file for writing
    with open(output_file, "w") as f_out:
        # Loop over the lines of the input file
        for line in lines:
            # Check if the line contains a '?'
            if '?' not in line:
                # Write the line to the output file
                f_out.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean a data file by removing lines with '?'")
    parser.add_argument("input_file", help="Path to the input data file")
    parser.add_argument("output_file", help="Path to the cleaned output data file")

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    clean_file(input_file, output_file)
