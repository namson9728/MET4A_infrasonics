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

def interferometric_response(data_collection, plot_title:str=None):
    """
    Parameters
    ----------

    Returns
    -------
    """
    fig, ax = plt.subplots(6, sharex=True, sharey=False, figsize=(10, 9))

    time_unit = data_collection['specifications']['units']['times']
    fig.supxlabel('Time (%s)' % time_unit)   

    fig.supylabel('Excess Wavelengths (deg)')

    plot_title = 'Interferometric Reponse' if plot_title == None else plot_title 
    fig.suptitle(plot_title)

    count = 0
    for stations in data_collection['excess_path_length'].keys():
        ax[count].plot(data_collection['times'], data_collection['excess_path_length'][stations]*360.0)
        
        ax[count].set_title(stations)
        count+=1

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

    for key in data_dict['data'].keys():
        p_arr = data_dict['data'][key]['pressures']
        time_arr = data_dict['data'][key]['times']

        plt.plot(time_arr, (np.array(p_arr) - np.mean(p_arr)))

    plt.legend(data_dict['specifications']['stations'],
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