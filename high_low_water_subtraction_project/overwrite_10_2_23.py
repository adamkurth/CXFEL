import os
import random
import string
import shutil
import numpy as np
import h5py as h5

print(os.getcwd())
# os.chdir('/Users/adamkurth/Documents/vscode/CXFEL Image Analysis/CXFEL/high_low_water_subtraction_project')

############################################ 

def load_stream(stream_name):
    global data_columns
    
    data_columns = {
    'h':[], 'k':[], 'l':[],
    'I':[], 'sigmaI':[], 'peak':[], 'background':[],
    'fs':[],'ss':[], 'panel':[]}      
    
    reading_peaks = False
    reading_geometry = False
    reading_chunks = True 
    
    try:
        stream = open(stream_name, 'r') 
        print("\nLoaded file successfully.", stream_name, '\n')
    except Exception as e: 
        print("\nAn error has occurred in load method:", str(e),'\n')
   
    for line in stream:
        if reading_chunks:
           if line.startswith('End of peak list'):
               reading_peaks = False
           elif line.startswith("   h    k    l          I   sigma(I)       peak background  fs/px  ss/px panel"):
               reading_peaks = True
           elif reading_peaks:
                try:
                    elements = line.split()
                    data_columns['h'].append(int(elements[0]))
                    data_columns['k'].append(int(elements[1]))
                    data_columns['l'].append(int(elements[2]))
                    data_columns['I'].append(float(elements[3]))
                    data_columns['sigmaI'].append(float(elements[4]))
                    data_columns['peak'].append(float(elements[5]))
                    data_columns['background'].append(float(elements[6]))
                    data_columns['fs'].append(float(elements[7]))
                    data_columns['ss'].append(float(elements[8]))
                    data_columns['panel'].append(str(elements[9]))
                except:
                    pass
        elif line.startswith('----- End geometry file -----'):
            reading_geometry = False
        elif reading_geometry:   
            try:
                par, val = line.split('=')
                if par.split('/')[-1].strip() == 'max_fs' and int(val) > max_fs:
                    max_fs = int(val)
                elif par.split('/')[-1].strip() == 'max_ss' and int(val) > max_ss:
                    max_ss = int(val)
            except ValueError:
                pass
        elif line.startswith('----- Begin geometry file -----'):
            reading_geometry = True
        elif line.startswith('----- Begin chunk -----'):
            reading_chunks = True   
    return data_columns

#############################################

def retrieve(data_columns, *args):
    # taking in data_columns and selecting the desired columns to retrieve
    return [data_columns[col] for col in args if col in data_columns]

#############################################

def duplicate_before_overwrite(filename):
    # taking filename and adding copy extension to it.
    base_file, extension = filename.rsplit('.',1)
    new_base_file = f'{base_file}_copy'
    new_filename = f'{new_base_file}.{extension}'
    duplicate = shutil.copyfile(filename, new_filename)
    return duplicate

#############################################

def compare_high_low(high_data, low_data, *cols_to_compare):
    """
    Compare the high and low intensity data.
    """
    if not cols_to_compare:
        cols_to_compare = high_data.keys()
    compared_data = {}
    for col in cols_to_compare:
        if col in high_data and col in low_data:
            print(f'Comparing {col}: \n')
            print(f'High: {high_data[col]} \n')
            print(f'Low: {low_data[col]} \n')
            print()
            compared_data[col] = (high_data[col], low_data[col])
    return compared_data

#############################################

def overwrite_low_in_high(filename, overwrite_data):
    with open(filename, 'r') as f:
        lines = f.readlines()

    with open(filename, 'r+') as f:
        for line in lines:
            if line.startswith("   h    k    l          I   sigma(I)       peak background  fs/px  ss/px panel"):
                f.write(line)
                for i in range(len(overwrite_data['h'])):
                    formatted_row = '{:>4} {:>4} {:>4} {:>9} {:>12} {:>12} {:>12} {:>6} {:>6} {:>6}\n'.format(
                        overwrite_data['h'][i], 
                        overwrite_data['k'][i], 
                        overwrite_data['l'][i], 
                        overwrite_data['I'][i], 
                        overwrite_data['sigmaI'][i], 
                        overwrite_data['peak'][i], 
                        overwrite_data['background'][i], 
                        overwrite_data['fs'][i], 
                        overwrite_data['ss'][i], 
                        overwrite_data['panel'][i]
                    )
                    f.write(formatted_row)
            else:
                # Write the unmodified line to the file
                f.write(line)
                
#############################################

def intensity_finder(x_coords, y_coords, image_name):
    import h5py as h5
    import numpy as np  
    """
    Retrieve the intensity values for every x,y coordinate in the image.
    """
    with h5.File(image_name, "r") as f: 
        intensities = f['/entry/data/data'][()]
    intensities = np.array(intensities)
    found_intensities = []
    # xmin, xmax = min(x_coords), max(x_coords)
    # ymin, ymax = min(y_coords), max(y_coords)
    for x,y in zip(x_coords, y_coords):
        if x < intensities.shape[0] and y < intensities.shape[1]:
            found_intensities.append(intensities[int(x), int(y)])
    # print(found_intensities)
    return found_intensities

#############################################

def populate_intensity_array(data_columns, image_name):
    """
    Populate the intensity array with the intensity values for each x,y coordinate.
    """
    with h5.File(image_name, "r") as f: 
        intensities = f['/entry/data/data'][()]
    intensities = np.array(intensities)
    
    new_intensities = np.zeros((intensities.shape[0], intensities.shape[1]))
    
    for i in range(len(data_columns['fs'])):
        x = int(data_columns['fs'][i])
        y = int(data_columns['ss'][i])
        if x < intensities.shape[0] and y < intensities.shape[1]:
            new_intensities[x][y] = intensities[x][y]
    return new_intensities
    
#############################################
    
    
    

# xmin, xmax = min(data_columns['fs']), max(data_columns['fs'])
# ymin, ymax = min(data_columns['ss']), max(data_columns['ss'])
# intensity_array = np.zeros((int(xmax-xmin), int(ymax-ymin)))
# intensities = intensity_finder(data_columns['fs'], data_columns['ss'], image_name)
# for i in range(len(data_columns['fs'])):
#     x = int(data_columns['fs'][i] - xmin)
#     y = int(data_columns['ss'][i] - ymin)
#     if x < intensity_array.shape[0] and y < intensity_array.shape[1]:
#         intensity_array[x][y] = intensities[i]
# return intensity_array

#############################################

global intensity_array
high_stream_name = 'test_high_copy.stream'
low_stream_name = 'test_low_copy.stream'

high_data = load_stream(high_stream_name)
low_data = load_stream(low_stream_name)
# compare_high_low(high_data, low_data)

#Took low data from low_stream and put in high_stream file. 
overwrite_data = low_data
# overwrite_low_in_high(high_stream_name, overwrite_data)

#now high_stream has data from low_stream.
image_name = "9_18_23_high_intensity_3e8keV-1_test.h5"
## retrieved from stream coordinate menu
columns = ['fs', 'ss']

intensities = intensity_finder(high_data['fs'], high_data['ss'], image_name)
intensities_array = populate_intensity_array(high_data, image_name)
print(intensities_array)


# xmin, xmax = min(high_data['fs']), max(high_data['fs'])
# ymin, ymax = min(high_data['ss']), max(high_data['ss'])
# intensity_array = np.zeros((int(xmax-xmin), int(ymax-ymin)))


# for i in range(len(high_data['fs'])):
#     x,y = high_data['fs'][i], high_data['ss'][i]
#     z = intensities[i]
#     if x < intensity_array.shape[0] and y < intensity_array.shape[1]:
#         intensity_array[int(x)][int(y)] = z
            
    # x = int(high_data['fs'][i] - xmin)
    # y = int(high_data['ss'][i] - ymin)
    # if x < intensity_array.shape[0] and y < intensity_array.shape[1]:
    #     print(intensities)
        # intensity_array[x][y] = intensities[i]
        # z = intensity_array[x][y]
        # print("x:", x, "y:", y, "z:", z)

# print(intensity_array.shape, int(xmax-xmin), int(ymax-ymin))

# intervention
# currently what this does is take the data from high intensity stores it in a dictionary, and "overwrites" the dictonary with the low intensity data.
# We want to then actually take the low intensity data and and find the intensities for the correspoding x,y coordinates in the high data.
# retrieve these coordinates
# 

