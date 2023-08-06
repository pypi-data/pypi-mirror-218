# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 2023

@author: Luis Alfonso Olivares Jimenez

Tools to read 1-dimensional dose profiles and perform gamma index comparison.

The data should be in M ​​rows by 2 columns, corresponding to positions and
dose values, respectively.

The script has been tested with the following examples:

    * File in w2CAD format (format used by the TPS Eclipse 16.1, from the Varian(R) company).
      In the algorithm, the start of the data is identified by the words: '$STOM' or '$STOD'
      Physical unit assumed to be in mm.

    * File in mcc format (format used by Verisoft 7.1.0.199 software, from PTW(R) company).
      In the algorithm, the beginning of the data is identified by the word: 'BEGIN_DATA'
      Physical unit assumed to be in mm.

    * File in text format
      The data must be distributed in M ​​rows by 2 columns and separated
      for a blank space.
      The script ask for a word to identify the beginning of the data in the text file, 
      a number to add to the positions, and a factor for distance dimension conversion.

"""

import numpy as np

def text_to_list(file_name):
    """
    Convert a text file to a python list. Each element of the list 
    represents a line from the text file.

    Parameters
    ----------

    file_name : string
        Text file name
    
    Returns
    -------

    list
        Loaded data as a list.
    
    """
    with open(file_name, encoding='UTF-8', mode = 'r') as file:
        data_list = [line.strip() for line in file]    
    return data_list


def identify_format(data_list):
    """
    Identify text format.

    Parameters
    ----------

    data_list : list
        Each element of the list represents a line from the text file.

    Returns
    -------

    string
        'varian' for w2CAD format, identified by the '$' character at the beginning of the file.

        'ptw' for mcc fromat, identified by the word 'BEGIN_SCAN_DATA'.

        'just_numbers' for data without headers.
        
        'text_file' for other formats. 

    """

    if data_list[0][0] == '$':
        return 'varian'

    elif data_list[0] == 'BEGIN_SCAN_DATA':
        return 'ptw'
    
    else: 
        is_a_number = data_list[0].split()[0]
        try:
            float(is_a_number)
            return 'just_numbers'
        
        except ValueError:
            return 'text_file'


def get_data(file_name, 
             start_word = None, 
             end_word = None,
             delta = None):
    
    """
    Get and normalize data from a text-file (file that is structured as a sequence of lines).
    Since w2CAD and mcc formats are automatically detected, it is not necessary 
    to specify start/end words in such cases.
    
    Parameters
    ----------

    file_name : string
        Name of the file

    start_word : string 
        Word to identify the beginning of the data

    end_word : string 
        Word to identify the end of the data

    delta : float 
        Displacement in mm to define the started point
    
        
    Returns
    -------

    ndarray
        Data as a Numpy object
    
    """

    all_list = text_to_list(file_name)
    file_format = identify_format(all_list)
    

    #   w2CAD format (Varian)
    
    if file_format == 'varian':
        if '$STOM' in all_list:
            start_index = all_list.index('$STOM') + 1
            end_index = all_list.index('$ENOM')         #Find the beginning and end of the data
            
        elif '$STOD' in all_list:
            start_index = all_list.index('$STOD') + 1
            end_index = all_list.index('$ENOD')
            
        data_list = all_list[start_index: end_index]
        # Extraer datos de las lineas que comienzan con el caracter '<'
        data_list = [idx[1:-1].split() for idx in data_list if idx[0] == "<"]
        data_array = np.array(data_list).astype(float)
        data_array[:,1] = 100*data_array[:,1]/np.amax(data_array[:,1])
        

    #   mcc format (PTW)     

    elif file_format == 'ptw':

        start_index = all_list.index('BEGIN_DATA') + 1  
        end_index = all_list.index('END_DATA')          #Find the beginning and end of the data
        
        data_list = all_list[start_index: end_index]
        data_list = [line.split() for line in data_list]
        data_array = np.array(data_list).astype(float)
        data_array[:,1] = 100*data_array[:,1]/np.amax(data_array[:,1])
        data_array = data_array[:,0:2]


    #   User defined words to identify start and end of the data

    else:
        if start_word != None:
            if start_word in all_list:
                start_index = all_list.index(start_word) + 1
            else: 
                print("Start word not found in the file")
        else:
            start_index = 0
            
        if end_word != None:
            if end_word in all_list:
                end_index = all_list.index(end_word)
            else:
                print("End word not found in the file")
        else: 
            end_index = len(all_list) - 1
        
        data_list = all_list[start_index: end_index]
        data_list = [line.split() for line in data_list]
        data_array = np.array(data_list).astype(float)
        data_array[:,1] = 100*data_array[:,1]/np.amax(data_array[:,1])
    
    if delta != None:
        data_array[:,0] = data_array[:,0] + float(delta)
        
    
    return data_array


def build_from_array_and_step(array, step):
    """Create a new array with the same length but with an additional axis. The first column represents the 
    physical positions of the given values. The second column is a normalization of the given array. 
    The positions are builded with evenly step spacing starting from zero.

    Parameters
    ----------

    array : ndarrya,
        Numpy 1D array with the profile values

    step : float,
        The spacing between samples

    Returns
    -------

    array, ndarray
        A new array with shape (M,2), where M is the shape of the array.

    Examples
    --------

    >>> y = np.array([2,4,6,8,10])
    >>> A = build_from_array_and_step(y, 0.5)
    [ 
    [0.0, 2] 
    [0.5, 4]         
    [1.0, 6]
    [1.5, 8]
    [2.0, 10]]

    >>> y = np.arange(6)
    >>> B = build_from_array_and_step(y, 3)
    [
    [0, 0]
    [3, 1]
    [6, 2]
    [9, 3]
    [12, 4]]

    """

    num = array.shape[0]
    start = 0
    stop = (num - 1) * step

    positions = np.linspace(start, stop, num = num, endpoint = True)
    profile = np.zeros((num, 2))
    profile[:,0] = positions
    profile[:,1] = array / np.max(array) * 100

    return profile
    

def gamma_1D(ref, eval, dose_t = 3, dist_t = 2, dose_threshold = 0, interpol = 1):
    '''
    1-dimensional gamma index calculation.
    Dose profiles have to be normalized (0-100%).

    Parameters
    ----------

    ref : ndarray,
        Reference dose profile represented by a (M, 2) numpy array.  

    eva : ndarray,
        Dose profile to be evaluated, represented by a (N, 2) numpy array.  

    dose_t : float, default = 3
            Dose tolerance [%].

    dist_t : float, default = 2
        Distance to agreement [mm].

    dose_threshold : float, default = 0
        Dose threshold [%].
        Any point in the distribution with a dose value less than the threshold 
        is going to be excluded from the analysis.
    
    interpol : float, default = 1
        Number of interpolated points to generate between each two consecutive points in "eval" data.

    Returns
    -------

    ndarray, float
        gamma distribution, gamma percent and number of evaluated points
        
    '''

    # min_position and max_position to analyze.
    min_position = np.max( (np.min(ref[:,0]), np.min([eval[:,0]])) )
    max_position = np.min( (np.max(ref[:,0]), np.max([eval[:,0]])) ) 

    num_of_points = eval.shape[0]
    interp_positions = np.linspace(ref[0,0], ref[-1,0], (interpol + 1)*(num_of_points - 1) + 1, endpoint=True)
    eval_from_interp_positions = np.interp(interp_positions, eval[:,0], eval[:,1], left = np.nan, right = np.nan) 
    add_positions = np.array((interp_positions, eval_from_interp_positions))
    eval_from_interp_positions = np.transpose(add_positions)

    #   A variable to store gamma calculations.
    gamma = np.zeros( (ref.shape[0], 2) )

    gamma[:,0] = ref[:,0]   #Add the same positions.

    for i in range(ref.shape[0]):

        if (ref[i,0] < min_position) or (ref[i,0] > max_position):  

            gamma[i, 1] = np.nan
            continue

        Gamma_appended = np.array([])  #   Gamma calculation for each point in "ref" data.
        for j in range(eval_from_interp_positions.shape[0]):

            dose_difference = ref[i,1] - eval_from_interp_positions[j,1]
            distance = ref[i,0] - eval_from_interp_positions[j,0]

            Gamma = np.sqrt(
                        (distance**2) / (dist_t**2)
                        + (dose_difference**2) / (dose_t**2))
                        
            Gamma_appended = np.append(Gamma_appended, Gamma)

        gamma[i,1] = np.min( Gamma_appended[ ~np.isnan(Gamma_appended) ] )
        if ref[i,1] < dose_threshold:
            gamma[i,1] = np.nan

    # Coordinates for gamma values <= 1.
    less_than_1_coordinate = np.where(gamma[:,1] <= 1)
    # Number of points where gamma <= 1.
    less_than_1 = np.shape(less_than_1_coordinate)[1]
    # Number evaluated points (!= nan)
    evaluated_points = np.shape(gamma)[0] - np.shape(np.where(np.isnan(gamma[:,1])))[1]
    
    gamma_percent = float(less_than_1)/evaluated_points*100

    return gamma, gamma_percent, evaluated_points


if __name__ == '__main__':
    """
    y = np.array([2,4,6,8,10])
    A = build_from_array_and_step(y, 0.5)
    print(A)

    y = np.arange(10)
    B = build_from_array_and_step(y, 3)
    print(B)

    """
    #Test files
    file_name = './test_data/test_ptw.mcc'
    #file_name = './test_data/test_varian.data'
    #file_name = './test_data/test_txt.txt'

    file_name_eval = "./test_data/X06 OPEN 10X10 PDD WAT 221214 13'13'42.mcc"
    
    data_ref = get_data(file_name, start_word =  'Field 1')
    data_eval = get_data(file_name_eval)
    g, gp = gamma_1D(data_ref, data_eval)
    print(gp)
