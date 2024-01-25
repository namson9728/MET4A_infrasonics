import numpy as np
import matplotlib.pyplot as plt

"""
A class that contains all the methods to generate specific plots given the dataset

...

Methods
-------
interferometric_response( FIX ME! )
    Generates a 'interferometric response vs. time' plot for all bandwidths

allan_variance( FIX ME! )
    Generates a 'phase vs. time' plot of the Allan variance for all bandwidths

correlation( FIX ME! )
    Generates a 'amplitude vs. frequency' plot of each cross correlation

time_series( FIX ME! )
    Generates a 'pressure vs. time' plot of the dataset(s)

masterplot( FIX ME! )
    Generates a comprehensive plot of the timeseries, correlation, Allan variance, and interferometric response
    
"""

def interferometric_response():
    """
    Parameters
    ----------

    Returns
    -------
    """
    return -1

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

def time_series(data_dict, plot_title:str='Pressure Response'):
    """Generates a time series plot of the data collection

    Parameters
    ----------
    data_dict : dict
        A properly formatted dictionary containing both 'specifications' and 'data' of the collection
    plot_title : str
        The title for the time series plot
        (default: 'Pressure Response')
    """
    plt.figure(figsize=(15, 10))
    plt.rc('xtick', labelsize=20) 
    plt.rc('ytick', labelsize=20) 
    
    stations = []
    for key in data_dict['data'].keys():
        p_arr = data_dict['data'][key]['pressures']
        time_arr = data_dict['data'][key]['times']

        stations.append(key)

        plt.plot(time_arr, (np.array(p_arr) - np.mean(p_arr)))

    plt.legend(stations,
        bbox_to_anchor=(1.125, 1.0),
        loc='upper right', fontsize=20)

    filter_num = str(data_dict['specifications']['filter'])
    plt.title(plot_title + ' %s' % filter_num, fontsize=40)

    time_unit = str(data_dict['specifications']['units']['times'])
    plt.xlabel('Time (%s)' % time_unit, fontsize=40)

    pressure_unit = str(data_dict['specifications']['units']['pressures'])
    plt.ylabel('Pressure (%s)' % pressure_unit, fontsize=40)

def master_plot():
    """
    Parameters
    ----------

    Returns
    -------
    """
    return -1