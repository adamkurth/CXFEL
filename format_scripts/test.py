import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os, sys
import test as t
# Research Question: whether there is a linear dependence of X-ray diffraction intensities on the number of unit cells exposed to the X-rays.

# input_data
# h, k, l = orientation of the crystal lattice planes in three-dimensional reciprocal space
# FREE = which reflections were used for the refinement
# FP = the observed structure factor amplitudes, (observed/measured amplitudes of the structure factors)
# SIGFP = the estimated standard deviations of the observed structure factor amplitudes
# FC = model-based structure factor amplitudes
# PHIC = calculated phase angles associated with the FC column
# FC_ALL, PHIC_ALL = additional structure factor amplitudes and phase angles (useful for refinement/model building)
# DELFWT, PHDELWT = difference in Fourier coefficients (also used for model building/refinement)
# FOM = figure of merit (FOM), quantifies the reliability of point estimates
# FC_ALL_LS, PHIC_ALL_LS = represents the least square Fourier coefficients (map calculations)

# output_data
# h, k, l = orientation of the crystal lattice planes in three-dimensional reciprocal space
# FP (observed) = observed structure factor amplitudes (experimentally measured values of diffraction patterns)
        # provide information about the strength of the reflections in the diffraction pattern
# SIGFP (Sigma-Fobserved) = estimated standard deviations of the observed amplitudes (FP), indicate uncertainty in the observed amplitudes  
# FC (Fcalc) = calculated structure factor amplitudes based on the model (predicted by a structure model compared to observed amplitudes (FP) during refinement process)
# PHIC (PHIcalc) = calculated phase angles associated with the FC column (used in calculating electron density maps)
 
# FP and FC contain information about the observed and calculated structure factor amplitudes.


def analyze_crystal(pdb_name, input_name, output_name):
    # Set the working directory
    working_dir = "/Users/adamkurth/Documents/vscode/CXFEL Image Analysis/CXFEL/unitcell_project"
    
    # Retrieve the pdb data
    pdb_path = f"{working_dir}/formatted_data/pdb_files/{pdb_name}"
    with open(pdb_path, "r", encoding="utf-8") as pdb_file:
        pdb_lines = pdb_file.read().splitlines()

    # Extract CRYST1 line
    cryst_line = next(line for line in pdb_lines if line.startswith("CRYST1"))
    cryst_components = cryst_line.split()

    # Dimension lengths
    a = float(cryst_components[1])
    b = float(cryst_components[2])
    c = float(cryst_components[3])

    # Angles (in degrees)
    alpha = float(cryst_components[4])
    beta = float(cryst_components[5])
    gamma = float(cryst_components[6])
    
    global unit_cell_attributes
    unit_cell_attributes = {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}
    # Retrieve the input data
    input_path = f"{working_dir}/formatted_data/input_data/{input_name}"
    with open(input_path, "r", encoding="utf-8") as input_file:
        input_data = input_file.read().splitlines()
    # Skip any blank lines
    input_data = [line for line in input_data if line.strip() != ""]
    
    # Split the data and extract columns
    data_rows = [line.split() for line in input_data[1:]]
    
    h = [int(line[0]) for line in data_rows]
    k = [int(line[1]) for line in data_rows]
    l = [int(line[2]) for line in data_rows]
    free = [int(line[3]) for line in data_rows]
    fp = [float(line[4]) for line in data_rows]
    sigfp = [float(line[5]) for line in data_rows]
    fc = [float(line[6]) for line in data_rows]
    phic = [float(line[7]) for line in data_rows]
    fc_all = [float(line[8]) for line in data_rows]
    phic_all = [float(line[9]) for line in data_rows]
    fwt = [float(line[10]) for line in data_rows]
    phwt = [float(line[11]) for line in data_rows]
    delfwt = [float(line[12]) for line in data_rows]
    phdelfwt = [float(line[13]) for line in data_rows]
    fom = [float(line[14]) for line in data_rows]
    fc_all_ls = [float(line[15]) for line in data_rows]
    phic_all_ls = [float(line[16]) for line in data_rows]
    
    column_names = ['h', 'k', 'l', 'FREE', 'FP', 'SIGFP', 'FC', 'PHIC', 'FC_ALL', 'PHIC_ALL', 'FWT', 'PHWT', 'DELFWT', 'PHDELWT', 'FOM', 'FC_ALL_LS', 'PHIC_ALL_LS']
    data_dict = {'h': h, 'k': k, 'l': l, 'FREE': free, 'FP': fp, 'SIGFP': sigfp, 'FC': fc, 'PHIC': phic, 'FC_ALL': fc_all, 'PHIC_ALL': phic_all, 'FWT': fwt, 'PHWT': phwt, 'DELFWT': delfwt, 'PHDELWT': phdelfwt, 'FOM': fom, 'FC_ALL_LS': fc_all_ls, 'PHIC_ALL_LS': phic_all_ls}
    df_in = pd.DataFrame(data_dict)
    
    
    calculateVolume(alpha, beta, gamma, a, b, c, df_in)
    
    # Retrieve the output data
    output_path = f"{working_dir}/formatted_data/output_data/{output_name}"
    with open(output_path, "r", encoding="utf-8") as output_file:
        output_data = output_file.read().splitlines()

    # Skip any blank lines
    output_data = [line for line in output_data if line.strip() != ""]

    # Split the data and extract columns
    data_rows = [line.split() for line in output_data[1:]]
    h = [int(line[0]) for line in data_rows]
    k = [int(line[1]) for line in data_rows]
    l = [int(line[2]) for line in data_rows]
    free = [int(line[3]) for line in data_rows]
    fp = [float(line[4]) for line in data_rows]
    sigfp = [float(line[5]) for line in data_rows]
    fcalc = [float(line[6]) for line in data_rows]
    phicalc = [float(line[7]) for line in data_rows]
    
    data_dict = {'h': h, 'k': k, 'l': l, 'FREE': free, 'FP': fp, 'SIGFP': sigfp, 'FCalc': fcalc, 'PHICalc': phicalc}
    df_out = pd.DataFrame(data_dict)    
    # temp_array = np.array(data_rows)
    # col_names = ['h', 'k', 'l', 'FREE', 'FP', 'SIGFP', 'FCalc', 'PHICalc']
    # df_in = np.vstack((col_names, temp_array))
    
    return df_in, df_out, unit_cell_attributes  

def calculateVolume(alpha, beta, gamma, a, b, c, df_in):
    # Calculate unit cell volume (monoclinic)
    unitcell_vol = a * b * c
    # Calculate the volume of the parallelepiped
    crystal_vol = a * b * c * np.sqrt(1 - np.cos(np.deg2rad(alpha))**2 - np.cos(np.deg2rad(beta))**2 - np.cos(np.deg2rad(gamma))**2 + 2 * np.cos(np.deg2rad(alpha)) * np.cos(np.deg2rad(beta)) * np.cos(np.deg2rad(gamma)))
    df_in['UnitCellVolume'] = unitcell_vol
    df_in['CrystalVolume'] = crystal_vol
    df_in['VolumeToUnitCellVolRatio'] = df_in['CrystalVolume'] / df_in['UnitCellVolume']
    return df_in

def plot(x_col, y_col, df, x_label=None, y_label=None, title=None):
    plt.scatter(df[x_col], df[y_col])
    if x_label:
        plt.xlabel(x_label)
    else:
        plt.xlabel(x_col)
    if y_label:
        plt.ylabel(y_label)
    else:
        plt.ylabel(y_col)
    if title:
        plt.title(title)
    else:
        plt.title(f"{y_col} vs {x_col}")
    plt.show()

def linear_model(x_cols, y_col, df_in, df_out):
    # Create a linear regression model
    X = df_in[x_cols]
    y = df_out[y_col]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    # Print the model summary
    print(model.summary())

    # Plot the data and the regression line
    fig, ax = plt.subplots()
    ax.scatter(df_in[x_cols[0]], df_out[y_col])
    ax.plot(df_in[x_cols[0]], model.predict(X), color='red')
    ax.set_xlabel(x_cols[0])
    ax.set_ylabel(y_col)
    for i in range(1, len(x_cols)):
        ax.scatter(df_in[x_cols[i]], df_out[y_col])
        ax.plot(df_in[x_cols[i]], model.predict(X), color='red')
        ax.set_xlabel(x_cols[i])
    ax.set_title(f"{y_col} vs {', '.join(x_cols)}")

    # Plot the error bars
    y_pred = model.predict(X)
    y_err = y - y_pred
    # ax.errorbar(df_in[x_cols[0]], y_pred, yerr=abs(y_err), fmt='o', color='red', ecolor='red', capsize=5, capthick=2, linestyle='dotted')
    plt.show()

    return model

def plot_residuals(model, x_cols, y_col, df_in, df_out):
    """
    Plots the residuals of a linear regression model.

    Parameters:
    model (statsmodels.regression.linear_model.RegressionResultsWrapper): The linear regression model.
    x_col (str): The name of the independent variable column.
    y_col (str): The name of the dependent variable column.
    df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
    None
    """
    fig, ax = plt.subplots()
    ax.scatter(df_in[x_cols], model.resid)
    ax.axhline(y=0, color='r', linestyle='-')
    ax.set_xlabel(x_cols)
    ax.set_ylabel("Residuals")
    ax.set_title(f"Residuals vs {x_cols}")
    err = np.std(model.resid)
    ax.errorbar(df_in[x_cols], model.resid, yerr=err, fmt='o', color='blue', ecolor='green', capsize=5, capthick=2)
    for i, val in enumerate(model.resid):
        ax.annotate(round(val, 2), (df_in[x_cols][i], val), textcoords="offset points", xytext=(0,10), ha='center')
    plt.show()
    
def create_crystal_df(crystal_names, dfs_in, unit_cells, dfs_out):
    # Initialize an empty DataFrame to hold the results
    results_df = pd.DataFrame(columns=['Crystal', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'Unit Cell Volume', 'Crystal Volume', 'VolumeToUnitCellVolRatio', 'Mean FP'])

    # Loop over the crystal names and dataframes
    for i, name in enumerate(crystal_names):
        # Calculate the unit cell volume and crystal volume
        a, b, c, alpha, beta, gamma = unit_cells[i].values()
        unit_cell_volume = dfs_in[i]['UnitCellVolume'].iloc[0]
        crystal_volume = dfs_in[i]['CrystalVolume'].iloc[0]
        ratio = dfs_in[i]['VolumeToUnitCellVolRatio'].iloc[0]

        # Calculate the mean FP value
        mean_fp = dfs_out[i]['FP'].mean()

        # Create a new row for the crystal
        row = [name, a, b, c, alpha, beta, gamma, unit_cell_volume, crystal_volume, ratio, mean_fp]

        # Append the row to the results DataFrame
        results_df.loc[len(results_df)] = row

    results_df = results_df.round({'Unit Cell Volume': 2, 'Crystal Volume': 2, 'VolumeToUnitCellVolRatio': 3, 'Mean FP': 3})
    return results_df

# if __name__ == "__main__":
#     # Example usage:
df_in_c1, df_out_c1, unit_cell_c1 = analyze_crystal("104m.pdb", "104m_input_formatted.txt", "104m_hkl_out_formatted.txt")
df_in_c2, df_out_c2, unit_cell_c2 = analyze_crystal("137l.pdb", "137l_input_formatted.txt", "137l_hkl_out_formatted.txt")
df_in_c3, df_out_c3, unit_cell_c3 = analyze_crystal("169l.pdb", "169l_input_formatted.txt", "169l_hkl_out_formatted.txt")
df_in_c4, df_out_c4, unit_cell_c4 = analyze_crystal("1a28.pdb", "1a28_input_formatted.txt", "1a28_hkl_out_formatted.txt")
df_in_c5, df_out_c5, unit_cell_c5 = analyze_crystal("1a2a.pdb", "1a2a_input_formatted.txt", "1a2a_hkl_out_formatted.txt")

df_in_c6, df_out_c6, unit_cell_c6 = analyze_crystal("19hc.pdb", "19hc_input_formatted.txt", "19hc_hkl_out_formatted.txt")
df_in_c7, df_out_c7, unit_cell_c7 = analyze_crystal("105m.pdb", "105m_input_formatted.txt", "105m_hkl_out_formatted.txt")
df_in_c8, df_out_c8, unit_cell_c8 = analyze_crystal("153l.pdb", "153l_input_formatted.txt", "153l_hkl_out_formatted.txt")
df_in_c9, df_out_c9, unit_cell_c9 = analyze_crystal("154l.pdb", "154l_input_formatted.txt", "154l_hkl_out_formatted.txt")
df_in_c10, df_out_c10, unit_cell_c10 = analyze_crystal("157d.pdb", "157d_input_formatted.txt", "157d_hkl_out_formatted.txt")
df_in_c11, df_out_c11, unit_cell_c11 = analyze_crystal("176l.pdb", "176l_input_formatted.txt", "176l_hkl_out_formatted.txt")
df_in_c12, df_out_c12, unit_cell_c12 = analyze_crystal("180l.pdb", "180l_input_formatted.txt", "180l_hkl_out_formatted.txt")


# plot("FP", "FC_ALL", df_in_c1, x_label="Volume to Unit Cell Volume Ratio", y_label="FP", title="FP vs Volume to Unit Cell Volume Ratio")
# linear_model(['FC_ALL', 'PHIC_ALL', 'VolumeToUnitCellVolRatio'], 'FCalc', df_in_c1, df_out_c1)

crystal_names = ['104m', '137l', '169l', '1a28', '1a2a', '19hc', '105m', '153l', '154l', '157d', '176l', '180l']
dfs_in = [df_in_c1, df_in_c2, df_in_c3, df_in_c4, df_in_c5, df_in_c6, df_in_c7, df_in_c8, df_in_c9, df_in_c10, df_in_c11, df_in_c12]
unit_cells = [unit_cell_c1, unit_cell_c2, unit_cell_c3, unit_cell_c4, unit_cell_c5, unit_cell_c6, unit_cell_c7, unit_cell_c8, unit_cell_c9, unit_cell_c10, unit_cell_c11, unit_cell_c12]
dfs_out = [df_out_c1, df_out_c2, df_out_c3, df_out_c4, df_out_c5, df_out_c6, df_out_c7, df_out_c8, df_out_c9, df_out_c10, df_out_c11, df_out_c12]

results_df = create_crystal_df(crystal_names, dfs_in, unit_cells, dfs_out)
print(results_df)

# shows slight linear relationship between FP and Volume to Unit Cell Volume Ratio
# linear_model(['VolumeToUnitCellVolRatio'], 'Mean FP', results_df, results_df)

# conditition number is large, indicates stable model
# lm = linear_model(['VolumeToUnitCellVolRatio'], 'Mean FP', results_df, results_df)

# plot_residuals(lm, 'VolumeToUnitCellVolRatio', 'Mean FP', results_df, results_df)

# sm.graphics.plot_fit(lm, 'VolumeToUnitCellVolRatio', vlines=True)

# Adding the total structure weights
t.main("104m.pdb")
