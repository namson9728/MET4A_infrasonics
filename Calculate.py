import numpy as np
import scipy as scp 

"""
A class that contains all the methods used to analyze the pressure data

...

Attributes
----------
dataset : Data
sampling_rate : int
    the sampling rate used during collection of the dataset
    (default 625)

Methods
-------
excess_path_length( FIX ME! )
    Calculates the excess path length values for all unique bandwidth combinations of the given pressure data collection

allan_variance( FIX ME! )
    Calculates the allan_variance values of the excess path length dataset

correlation( FIX ME! )
    Calculates the cross correlation values for all bandwidth combinations of the given pressure data collection
"""

def excess_path_length(data_collection, L_norm:float=2000, p_norm:float=1,
                       L_norm_units:str='mm', p_norm_units:str='bar'):
    """
    Parameters
    ----------

    Returns
    -------
    """
    excess_arr = {}
    stations = data_collection['specifications']['stations']
    for i in range(len(stations)):
        for j in range(i+1, len(stations)):
            
            p_arr1 = np.array(data_collection['data'][stations[i]]['pressures']) - np.mean(data_collection['data'][stations[i]]['pressures'])
            p_arr2 = np.array(data_collection['data'][stations[j]]['pressures']) - np.mean(data_collection['data'][stations[j]]['pressures'])

            key = str(stations[i] + '-' + stations[j])
            excess_arr[key] = np.array((p_arr1 - p_arr2) * (L_norm / p_norm))

        excess_lengths = {}
        excess_lengths['specifications'] = (data_collection['specifications'])
        excess_lengths['specifications']['units'] = {'L_norm':L_norm_units,
                                               'p_norm':p_norm_units,
                                               'times':data_collection['specifications']['units']['times']}
        excess_lengths['excess_path_length'] = excess_arr
        excess_lengths['times'] = data_collection['data'][stations[0]]['times']

    return excess_lengths

def allan_variance(data_collection:dict, allan_var_units:str='Phase'):
    """
    Parameters
    ----------

    Returns
    -------
    """
    t_arr = data_collection['times']
    t_arr = np.mean(np.diff(t_arr))

    bandwidths = {}
    for key, value in data_collection['excess_path_length'].items():
        allan_var = np.zeros(len(value))
        print("Starting data collection for " + key)

        for idx in range(1, len(value)//2):
            allan_var[idx] = np.mean((value[:-2*idx] - 2*value[idx:-idx] + value[idx*2:])**2.0) / (2.0 * (idx * t_arr) **2)

        bandwidths[key] = allan_var
    
    allan_var_dict = {}
    allan_var_dict['specifications'] = (data_collection['specifications'])
    allan_var_dict['specifications']['units'] = {'allan_var':allan_var_units,
                                                 'times':data_collection['specifications']['units']['times']}
    allan_var_dict['times'] = data_collection['times']
    allan_var_dict['allan_var'] = bandwidths

    return allan_var_dict

def correlation():
    """
    Parameters
    ----------

    Returns
    -------
    """
    return -1