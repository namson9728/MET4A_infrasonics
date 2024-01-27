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

        delta_data = {}
        delta_data['specifications'] = (data_collection['specifications'])
        delta_data['specifications']['units'] = {'L_norm':L_norm_units, 'p_norm':p_norm_units}
        delta_data['excess_path_length'] = excess_arr
        delta_data['times'] = data_collection['data'][stations[0]]['times']

    return delta_data

def allan_variance():
    """
    Parameters
    ----------

    Returns
    -------
    """
    return -1

def correlation():
    """
    Parameters
    ----------

    Returns
    -------
    """
    return -1