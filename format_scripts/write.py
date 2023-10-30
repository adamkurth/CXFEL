def write(results_df, intensity_df, spacegroup):
    # Write intensity data to file
    intensity_filename = f"{spacegroup}_intensity_data.txt"
    with open(intensity_filename, "w") as f:
        f.write(intensity_df.to_string())

    # Write crystal data to file
    crystal_filename = f"{spacegroup}_crystal_data.txt"
    with open(crystal_filename, "w") as f:
        f.write(results_df.to_string())
