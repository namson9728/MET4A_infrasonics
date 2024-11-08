"""
Plot
----
A class that contains all the methods to generate specific plots given the dataset

Methods
-------
interferometric_response(data_collection:dict, plot_title:str=None)
    Generates a ``Interferometric Response vs. Time`` plot for all station pairs

allan_variance(data_collection:dict, plot_title:str=None)
    Generates a ``Phase vs. Time`` plot of the Allan variance for all station pairs

correlation(data_collection:dict, amplitude_units:str='dB', plot_title:str=None)
    Generates a ``Amplitude vs. Frequency`` plot of each cross correlation

time_series(data_collection, plot_title:str=None)
    Generates a ``Pressure vs. Time`` plot of the dataset(s)

masterplot( FIX ME! )
    Generates a comprehensive plot of the timeseries, correlation, Allan variance, and interferometric response
    
"""

import numpy as np
import matplotlib.pyplot as plt

def interferometric_response(data_collection:dict, plot_title:str=None):
    """Plots the excess path length simulating the inferometric response where ``lambda_obs = 1``

    Parameters
    ----------
    data_collection: dict
        Collection with excess path length data

    plot_title : str
        The desired name for the plot
        (default ``Interferometric Reponse``)

    """
    fig, ax = plt.subplots(6, sharex=True, sharey=False, figsize=(10, 12))

    time_unit = data_collection['specifications']['units']['times']
    fig.supxlabel('Time (%s)' % time_unit, fontsize=15)   

    fig.supylabel('Excess Wavelengths (deg)', fontsize=15)

    plot_title = 'Interferometric Reponse' if plot_title == None else plot_title 
    fig.suptitle(plot_title, fontsize=20)

    count = 0
    for stations in data_collection['excess_path_length'].keys():
        ax[count].plot(data_collection['times'], data_collection['excess_path_length'][stations]*360.0)
        
        ax[count].set_title(stations)
        count+=1

    plt.subplots_adjust(left=0.1,
                        bottom=0.05, 
                        right=0.9, 
                        top=0.93, 
                        wspace=0.1, 
                        hspace=0.2)

def allan_variance(data_collection:dict, plot_title:str=None):
    """Plots the Allan variance data

    Parameters
    ----------
    data_collection : dict
        Collection with Allan variance data

    plot_title : str
        The desired name for the plot
        (default ``Allan Variance``)

    """
    fig,ax = plt.subplots(3, 2, figsize=(12, 17), sharey=True, sharex=True)
    plot_title = 'Allan Variance' if plot_title == None else plot_title 
    fig.suptitle(plot_title, fontsize=30)
    fig.supxlabel('Time (%s)' % data_collection['specifications']['units']['times'], fontsize=25)
    fig.supylabel('Phase', fontsize=25)

    count = 0
    for i in range(0,3):
        for j in range(0,2):
            bandwidths = list(data_collection['allan_var'].keys())
            delta_time = data_collection['specifications']['units']['delta_time']
            allan_var = data_collection['allan_var'][bandwidths[count]]

            ax[i][j].scatter(delta_time * np.arange(len(allan_var)), allan_var, label='Allan Variance', color='red')        
            ax[i][j].set_xscale('log')
            ax[i][j].set_yscale('log')
            ax[i][j].set_title(bandwidths[count], fontsize=15)
            # plot guidelines
            time_axis = delta_time * np.arange(len(allan_var))
            ax[i][j].plot(time_axis, time_axis**-2.0, label='delta_time**-2.0')
            ax[i][j].plot(time_axis, time_axis**-1.0, label='delta_time**-1.0')
            ax[i][j].plot(time_axis, time_axis**-0.5, label='delta_time**-0.5')

            ax[i][j].legend(loc='upper right', fontsize=12)
            count+=1

    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=0.06, 
                        right=0.9, 
                        top=0.93, 
                        wspace=0.1, 
                        hspace=0.1)

def correlation(data_collection:dict, amplitude_units:str='dB', plot_title:str=None):
    """Plots both the auto-correlation and cross-correlation of the data

    Parameters
    ----------
    data_collection : dict
        Collection with correlation data (both auto-correlation and cross-correlation)

    amplitude_units : str
        Units of amplitude
        (default ``dB``)

    plot_title : str
        The desired title for the plot
        (default ``CORRELATION``)
        
    """
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 15))
    plt.subplots_adjust(left=0.1,
                        bottom=0.06, 
                        right=0.9, 
                        top=0.93, 
                        wspace=0.1, 
                        hspace=0.1)
    plot_title = 'CORRELATION' if plot_title == None else plot_title
    fig.suptitle(plot_title, fontsize=30)
    fig.supxlabel('Frequency (%s)' % data_collection['specifications']['units']['frequency'], fontsize = 25)
    fig.supylabel('Amplitude (%s)' % amplitude_units, fontsize=25)
    plt.xscale('log')

    label_arr = []
    cross_pairs = list(data_collection['cross']['frequencies'].keys())
    for idx in range(len(cross_pairs)):
        cross_frequencies = data_collection['cross']['frequencies'][cross_pairs[idx]]
        cross_norm = data_collection['cross']['correlation_norm'][cross_pairs[idx]]

        ax[1].plot(cross_frequencies, abs(cross_norm))
        ax[1].set_title('Cross-Correlation Normalized', fontsize=20)
        ax[2].plot(cross_frequencies, 180.0/np.pi*(np.angle(cross_norm)))
        ax[2].set_title('Phase', fontsize=20)
        label_arr.append(cross_pairs[idx])
    plt.legend(label_arr,
        bbox_to_anchor=(0, 1.275),
        loc='lower left', fontsize=20)
    
    auto_pairs = list(data_collection['auto']['frequencies'].keys())
    for idx in range(len(auto_pairs)):
        auto_frequencies = data_collection['auto']['frequencies'][auto_pairs[idx]]
        auto = data_collection['auto']['correlation'][auto_pairs[idx]]

        ax[0].plot(auto_frequencies, 10*np.log10(np.abs(auto)))
        ax[0].set_title('Auto-Correlation Power Spectrum', fontsize=20)

def time_series(data_collection:dict, plot_title:str=None):
    """Generates a time series plot of the data collection

    Parameters
    ----------
    data_collection : dict
        A properly formatted dictionary containing both ``specifications`` and ``data`` of the collection
    
    plot_title : str
        The title for the time series plot
        (default ``Pressure Response``)
    """
    plt.figure(figsize=(15, 10))

    for key in data_collection['data'].keys():
        p_arr = data_collection['data'][key]['pressures']
        time_arr = data_collection['data'][key]['times']

        plt.plot(time_arr, (np.array(p_arr) - np.mean(p_arr)))

    plt.legend(data_collection['specifications']['stations'],
        bbox_to_anchor=(1.125, 1.0),
        loc='upper right', fontsize=20)

    plot_title = 'Pressure Response' if plot_title == None else plot_title
    filter_num = str(data_collection['specifications']['filter'])
    plt.title(plot_title + ' %s' % filter_num, fontsize=40)

    time_unit = str(data_collection['specifications']['units']['times'])
    plt.xlabel('Time (%s)' % time_unit, fontsize=40)

    pressure_unit = str(data_collection['specifications']['units']['pressures'])
    plt.ylabel('Pressure (%s)' % pressure_unit, fontsize=40)

def full_plot(data_collection:dict, contains_allan_var:bool):
    """
    Parameters
    ----------
    data_collection : dict
        The full data collection containing the pressure, excess path length, Allan variance, and correlation data
    
    contains_allan_var : bool
        The function will plot the ``Allan Variance`` if this variable is set to ``True``
        (default ``False``)

    """
    return -1