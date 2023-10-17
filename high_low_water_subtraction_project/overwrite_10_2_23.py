import os
import shutil
import numpy as np
import h5py as h5

print(os.getcwd())
# os.chdir('/Users/adamkurth/Documents/vscode/CXFEL Image Analysis/CXFEL/high_low_water_subtraction_project')

############################################ From Stream Script (below) #############################################
       
class PeakThresholdProcessor: 
    #self method
    def __init__(self, image_array, threshold_value=0):
        self.image_array = image_array
        self.threshold_value = threshold_value
    #setter for threshold value
    def set_threshold_value(self, new_threshold_value):
        self.threshold_value = new_threshold_value
    #getter for for above threshold
    def get_coordinates_above_threshold(self):  
        coordinates = np.argwhere(self.image_array > self.threshold_value)
        return coordinates
 
def extract_region(image_array, region_size, x_center, y_center):
    extract = ArrayRegion(image_array)
    extract.set_peak_coordinate(x_center,y_center)
    extract.set_region_size(region_size)
    np.set_printoptions(floatmode='fixed', precision=10)
    np.set_printoptions(edgeitems=3, suppress=True, linewidth=200)
    region = extract.get_region()
    return region      
class ArrayRegion:
    def __init__(self, array):
        self.array = array
        self.x_center = 0
        self.y_center = 0
        self.region_size = 0
        
    def set_peak_coordinate(self, x, y):
            self.x_center = x
            self.y_center = y

    def set_region_size(self, size):
        #limit that is printable in terminal
        self.region_size = size
        max_printable_region = min(self.array.shape[0], self.array.shape[1]) //2
        self.region_size = min(size, max_printable_region)
        
    def get_region(self):
        x_range = slice(self.x_center - self.region_size, self.x_center + self.region_size+1)
        y_range = slice(self.y_center - self.region_size, self.y_center + self.region_size+1)
        region = self.array[x_range, y_range]
        return region

def coordinate_menu(image_array, threshold_value, coordinates, radius): 
    print("\nCoordinates above given threshold:", threshold_value, 'with radius: ', radius)
    for i, (x, y) in enumerate(coordinates):
        print(f"{i + 1}. ({x}, {y})")
        
    while True:
        choice = input("\nWhich coordinate do you want to process? (or 'q' to quit)\n")
        if choice == "q":
            print("Exiting")
            break
        
        try: 
            count = int(choice)-1
            if 0 <= count < len(coordinates):
                x,y = coordinates[count]
                print(f"\nProcessing - ({x}, {y})")
                print('Printing 9x9 two-dimensional array\n')
                
                #creates visualization if the array, of chosen peak
                print(x,y)
                display_region = extract_region(image_array, region_size=4, x_center=x, y_center=y)
                
                print('DISPLAY REGION \n', display_region, '\n')
                
                #segment is the area with the given radius that's passed through the function.
                segment = extract_region(image_array, region_size=radius, x_center=x, y_center=y)
                print ('SEGMENT \n', segment, '\n')
                
                # COMMENTED OUT FOR NOW, EASE OF TESTING

                #returns boolean array of traversed values.
                bool_square = np.zeros_like(segment, dtype=bool)
                print('BOOLEAN: before traversing.', '\n', bool_square, '\n') 
            
                ######start 3 ring integration
                values_array = extract_region(image_array, region_size=radius, x_center=x, y_center=y)
                
                global avg_values, intensity_peak
                total_sum = 0; skipped_point = None; count = 0; intensity_peak = 0
                #traverses through (i = row) , (j = column)
                for col_index in range(values_array.shape[0]):
                    for row_index in range(values_array.shape[1]):
                        if values_array[row_index, col_index] >= 0:
                            count += 1
                            bool_square[row_index, col_index] = True
                            if row_index == radius and col_index == radius:
                                skipped_point = (row_index, col_index)  
                                intensity_peak = values_array[row_index, col_index]
                                print(f'Peak point to be skipped: ({row_index}, {col_index}) ', values_array[radius,radius])
                            elif abs(row_index - radius) <= 1 and abs(col_index - radius) <=1:
                                print(f'Passed (row, col) ({row_index}, {col_index})', values_array[row_index,col_index])
                                pass
                            else:
                                print(f'(row,col) ({row_index}, {col_index}) with a value of ', values_array[row_index, col_index])
                                total_sum += values_array[row_index, col_index]
                                
                print('\n######################')
                print(bool_square)
                print('Number of traversed cells', count)
                print('Peak point to be skipped:', skipped_point)
                print('Total sum:',total_sum)
                if count > 0:
                    avg_values = total_sum / count
                else: 
                    avg_values = "Could not divide by 0."
                print('Average surrounding peak:',avg_values)
                return avg_values,intensity_peak
                break
            else: 
                print("Invalid coordinate idex.")
        except ValueError:
            print("Invalid input. Enter a number of 'q' to quit.")

############################################ From Stream Script (above) #############################################

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

def duplicate_before_overwrite(filename):
    # taking filename and adding copy extension to it.
    base_file, extension = filename.rsplit('.',1)
    new_base_file = f'{base_file}_copy'
    new_filename = f'{new_base_file}.{extension}'
    duplicate = shutil.copyfile(filename, new_filename)
    return duplicate

#############################################

def compare_high_low(high_data, low_data, *columns):
    """
    Compare the high and low data and return the compared data.
    """
    compared_data = {}
    for col in columns:
        if col in high_data and col in low_data:
            print(f'High: {high_data[col]} \n')
            print(f'Low: {low_data[col]} \n')
            print()
            compared_data[col] = (high_data[col], low_data[col])
            retrieve(list(high_data), list(low_data), *columns)
    return compared_data

def retrieve(data_columns, *args):
    result = []
    try:
        # taking in data_columns and selecting the desired columns to retrieve
        result = [data_columns[col] for col in args if col in data_columns]
    except Exception as e:
        pass
    return result
#############################################


def overwrite_low_in_high(filename, overwrite_data):
    """
    Overwrite the low data in the high stream file with the given overwrite data.
    """
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


def intensity_finder(x_coords, y_coords, image_name):
    """
    Retrieve the intensity values for every x,y coordinate in the image.
    """
    with h5.File(image_name, "r") as f:
        intensities = f['/entry/data/data'][()]
    intensities = np.array(intensities)
    found_intensities = []
    for x, y in zip(x_coords, y_coords):
        if x < intensities.shape[0] and y < intensities.shape[1]:
            found_intensities.append(intensities[int(x), int(y)])
    return found_intensities


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

def coordinate_menu(image_array, threshold_value, coordinates, radius): 
    print("\nCoordinates above given threshold:", threshold_value, 'with radius: ', radius)
    for i, (x, y) in enumerate(coordinates):
        print(f"{i + 1}. ({x}, {y})")
        
    while True:
        choice = input("\nWhich coordinate do you want to process? (or 'q' to quit)\n")
        if choice == "q":
            print("Exiting")
            break
        
        try: 
            count = int(choice)-1
            if 0 <= count < len(coordinates):
                x,y = coordinates[count]
                print(f"\nProcessing - ({x}, {y})")
                print('Printing 9x9 two-dimensional array\n')
                
                #creates visualization if the array, of chosen peak
                print(x,y)
                display_region = extract_region(image_array, region_size=4, x_center=x, y_center=y)
                
                print('DISPLAY REGION \n', display_region, '\n')
                
                #segment is the area with the given radius that's passed through the function.
                segment = extract_region(image_array, region_size=radius, x_center=x, y_center=y)
                print ('SEGMENT \n', segment, '\n')
                
                # COMMENTED OUT FOR NOW, EASE OF TESTING

                #returns boolean array of traversed values.
                bool_square = np.zeros_like(segment, dtype=bool)
                print('BOOLEAN: before traversing.', '\n', bool_square, '\n') 
            
                ######start 3 ring integration
                values_array = extract_region(image_array, region_size=radius, x_center=x, y_center=y)
                
                #traverses through (i = row) , (j = column)         

                global avg_values, intensity_peak
                total_sum = 0; skipped_point = None; count = 0; intensity_peak = 0
                #traverses through (i = row) , (j = column)
                for col_index in range(values_array.shape[0]):
                    for row_index in range(values_array.shape[1]):
                        if values_array[row_index, col_index] >= 0:
                            count += 1
                            bool_square[row_index, col_index] = True
                            if row_index == radius and col_index == radius:
                                skipped_point = (row_index, col_index)  
                                intensity_peak = values_array[row_index, col_index]
                                print(f'Peak point to be skipped: ({row_index}, {col_index}) ', values_array[radius,radius])
                            elif abs(row_index - radius) <= 1 and abs(col_index - radius) <=1:
                                print(f'Passed (row, col) ({row_index}, {col_index})', values_array[row_index,col_index])
                                pass
                            else:
                                print(f'(row,col) ({row_index}, {col_index}) with a value of ', values_array[row_index, col_index])
                                total_sum += values_array[row_index, col_index]
                                
                print('\n######################')
                print(bool_square)
                print('Number of traversed cells', count)
                print('Peak point to be skipped:', skipped_point)
                print('Total sum:',total_sum)
                if count > 0:
                    avg_values = total_sum / count
                else: 
                    avg_values = "Could not divide by 0."
                print('Average surrounding peak:',avg_values)
                return avg_values,intensity_peak
                break
            else: 
                print("Invalid coordinate idex.")
        except ValueError:
            print("Invalid input. Enter a number of 'q' to quit.")
            
global intensity_array
high_stream_name = 'test_high_copy.stream'
low_stream_name = 'test_low_copy.stream'

high_data = load_stream(high_stream_name)
low_data = load_stream(low_stream_name)
# compare_high_low(high_data, low_data)

# Took low data from low_stream and put in high_stream file.
overwrite_data = low_data
overwrite_low_in_high(high_stream_name, overwrite_data)

########## compare any columns in data_columns
# compare_high_low(high_data, low_data, "h")

# now high_stream has data from low_stream.
image_name = "9_18_23_high_intensity_3e8keV-1_test.h5"
## retrieved from stream coordinate menu
columns = ['fs', 'ss']

intensities = intensity_finder(high_data['fs'], high_data['ss'], image_name)
intensities_array = populate_intensity_array(high_data, image_name)

print(np.count_nonzero(intensities_array))  # 1251 10/13/23

# compare_high_low(high_data, low_data, *columns)

#  intensity_array_overwrite
threshold = PeakThresholdProcessor(intensities_array, threshold_value=1e-5) # very low! 
print("Original threshold value: ", threshold.threshold_value, "\n")
coordinate_list = threshold.get_coordinates_above_threshold()


coordinate_menu(intensities_array, threshold_value=threshold.threshold_value, coordinates= coordinate_list, radius=4)
intensity = intensity_peak
avg = avg_values
spot_estimate_peak = intensity - avg
print("Peak Estimate for ring 3:", spot_estimate_peak, 'with radius of', 4)
