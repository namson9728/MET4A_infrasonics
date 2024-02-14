"""
Calculate
---------
A class that contains all the methods used to analyze the pressure data

Methods
-------
excess_path_length(data_collection, L_norm:float=2000, p_norm:float=1, L_norm_units:str='mm', p_norm_units:str='bar')
    Calculates the excess path length values for all unique station pairs of the given pressure data collection

allan_variance(data_collection:dict, allan_var_units:str='Phase')
    Calculates the Allan variance values of the excess path length data collection

cross_correlate(data_collection:dict, frequency_units:str='Hz')
    Calculates the cross-correlation values for all unique station pairs of the given pressure data collection

auto_correlate (data_collection:dict, frequency_units:str='Hz')
    Calculates the auto-correlation values of all stations of the given pressure data collection

correlate(data_collection:dict, frequency_units:str='Hz')
    Calculates both the cross and auto-correlation using ``cross_correlate()`` and ``auto_correlate()``
"""

import numpy as np

def excess_path_length(data_collection, L_norm:float=2000, p_norm:float=1,
                       L_norm_units:str='mm', p_norm_units:str='bar'):
    """
    Parameters
    ----------

    Returns
    -------
    """
    excess_dict = {}
    stations = data_collection['specifications']['stations']
    for i in range(len(stations)):
        for j in range(i+1, len(stations)):
            
            p_arr1 = np.array(data_collection['data'][stations[i]]['pressures']) - np.mean(data_collection['data'][stations[i]]['pressures'])
            p_arr2 = np.array(data_collection['data'][stations[j]]['pressures']) - np.mean(data_collection['data'][stations[j]]['pressures'])

            key = str(stations[i] + '-' + stations[j])
            excess_dict[key] = np.array((p_arr1 - p_arr2) * (L_norm / p_norm))

        excess_lengths = {}
        excess_lengths['specifications'] = (data_collection['specifications']).copy()
        excess_lengths['specifications']['units'] = {'L_norm':L_norm_units,
                                               'p_norm':p_norm_units,
                                               'times':data_collection['specifications']['units']['times'],
                                               'pressures':data_collection['specifications']['units']['pressures']}
        excess_lengths['excess_path_length'] = excess_dict
        excess_lengths['times'] = data_collection['data'][stations[0]]['times']

    return excess_lengths

def allan_variance(data_collection:dict, allan_var_units:str='Phase'):
    """Calculates the Allan variance of the excess path lengths
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
    allan_var_dict['specifications'] = (data_collection['specifications']).copy()
    allan_var_dict['specifications']['units'] = {'allan_var':allan_var_units,
                                                 'times':data_collection['specifications']['units']['times'],
                                                 'pressures':data_collection['specifications']['units']['pressures']}
    allan_var_dict['times'] = data_collection['times']
    allan_var_dict['allan_var'] = bandwidths

    return allan_var_dict

def cross_correlate(data_collection:dict, frequency_units:str='Hz'):
    """Calculates the cross-correlation of each station in the data_collection
    Parameters
    ----------
    data_collection : dict
        A data collection of the pressures

    frequency_units: str
        The frequency unit for the correlation
        (default ``Hz``)

    Returns
    -------
    correlate_dict : dict
        A new data_collection storing the cross-correlation data
        
    """
    stations = data_collection['specifications']['stations']
    correlate_dict = {}
    pair_frequencies = {}
    pair_norm_cross_smooth = {}
    pair_cross_smooth = {}

    for i in range(len(stations)):
        for j in range(i+1, len(stations)):

            station1 = data_collection['data'][stations[i]]['pressures']
            station2 = data_collection['data'][stations[j]]['pressures']
            station1 = (station1 - np.mean(station1))
            station2 = (station2 - np.mean(station2))
            
            cross_12 = (np.fft.fft(station1) * np.conj(np.fft.fft(station2)))
            cross_12 = cross_12[:int(len(station1)/2)]
            norm_cross_12 = cross_12/abs(cross_12)
            
            num_bins = int(np.ceil(np.log2(len(cross_12))))
            cross_12_smooth = np.zeros(num_bins, dtype=cross_12.dtype)
            norm_cross_12_smooth = np.zeros(num_bins, dtype=norm_cross_12.dtype)
            values = np.zeros(num_bins)
            for idx in range(num_bins):
                cross_12_smooth[idx] = np.mean(cross_12[2**(idx):2**(idx+1)])
                norm_cross_12_smooth[idx] = np.mean(norm_cross_12[2**(idx):2**(idx+1)])
                values[idx] = ((2**idx) + (2**(idx+1)))/2

            samplingFrequency = data_collection['specifications']['sampling_frequency']
            timePeriod  = len(cross_12)/samplingFrequency
            frequencies = values/timePeriod
        
            key = str(stations[i] + '-' + stations[j])
            
            pair_frequencies[key] = frequencies
            pair_cross_smooth[key] = norm_cross_12_smooth
            pair_norm_cross_smooth[key] = norm_cross_12_smooth

    correlate_dict['specifications'] = (data_collection['specifications']).copy()
    correlate_dict['specifications']['units'] = {'pressures':data_collection['specifications']['units']['pressures'],
                                                 'times':data_collection['specifications']['units']['times'],
                                                 'frequency':frequency_units}
    correlate_dict['frequencies'] = pair_frequencies
    correlate_dict['correlation_norm'] = pair_norm_cross_smooth
    correlate_dict['correlation'] = pair_cross_smooth
    
    return correlate_dict

def auto_correlate(data_collection:dict, frequency_units:str='Hz'):
    """Calculates the auto-correlation of each station in the data_collection
    Parameters
    ----------
    data_collection : dict
        A data collection of the pressures

    frequency_units: str
        The frequency unit for the correlation
        (default ``Hz``)

    Returns
    -------
    correlate_dict : dict
        A new data_collection storing the auto-correlation data

    """
    stations = data_collection['specifications']['stations']
    correlate_dict = {}
    pair_frequencies = {}
    pair_norm_cross_smooth = {}
    pair_cross_smooth = {}

    for i in range(len(stations)):
        station1 = data_collection['data'][stations[i]]['pressures']
        station1 = (station1 - np.mean(station1))
        
        cross_12 = (np.fft.fft(station1) * np.conj(np.fft.fft(station1)))
        cross_12 = cross_12[:int(len(station1)/2)]
        norm_cross_12 = cross_12/abs(cross_12)
        
        num_bins = int(np.ceil(np.log2(len(cross_12))))
        cross_12_smooth = np.zeros(num_bins, dtype=cross_12.dtype)
        norm_cross_12_smooth = np.zeros(num_bins, dtype=norm_cross_12.dtype)
        values = np.zeros(num_bins)
        for idx in range(num_bins):
            cross_12_smooth[idx] = np.mean(cross_12[2**(idx):2**(idx+1)])
            norm_cross_12_smooth[idx] = np.mean(norm_cross_12[2**(idx):2**(idx+1)])
            values[idx] = ((2**idx) + (2**(idx+1)))/2

        samplingFrequency = data_collection['specifications']['sampling_frequency']
        timePeriod  = len(cross_12)/samplingFrequency
        frequencies = values/timePeriod
    
        key = str(stations[i] + '-' + stations[i])
        
        pair_frequencies[key] = frequencies
        pair_cross_smooth[key] = norm_cross_12_smooth
        pair_norm_cross_smooth[key] = norm_cross_12_smooth

    correlate_dict['specifications'] = (data_collection['specifications']).copy()
    correlate_dict['specifications']['units'] = {'pressures':data_collection['specifications']['units']['pressures'],
                                                 'times':data_collection['specifications']['units']['times'],
                                                 'frequency':frequency_units}
    correlate_dict['frequencies'] = pair_frequencies
    correlate_dict['correlation_norm'] = pair_norm_cross_smooth
    correlate_dict['correlation'] = pair_cross_smooth
    
    return correlate_dict

def correlate(data_collection:dict, frequency_units:str='Hz'):
    """Calculates both the cross and auto-correlation of each station in the data_collection
    Parameters
    ----------
    data_collection : dict
        A data collection of the pressures

    frequency_units: str
        The frequency unit for the correlation
        (default ``Hz``)

    Returns
    -------
    correlate_dict : dict
        A new data_collection storing both the cross and auto-correlation data
        
    """
    cross = cross_correlate(data_collection, frequency_units)
    auto = auto_correlate(data_collection, frequency_units)

    correlate = {}
    correlate['specifications'] = (cross['specifications']).copy()
    correlate['cross'] = cross
    correlate['auto'] = auto

    return correlate