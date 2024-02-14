"""
DataCollection
--------------
There are two main data collection formats: standard and non-standard

As the name suggests, standard format is the standard way a data collection
is store to simplify the data analysis process.
```
standard_pressure_collection_format = {'specifications': {'filter_number':b'IA=%d',
                                                          'units': {'pressures':str,
                                                                    'times':str
                                                                   }
                                                          'stations':[],
                                                          'sampling_frequency':[]
                                                         },
                                       'data':{'pressures':[],
                                               'times':[]
                                              }
                                       }
```
Non-standard format refers to the original format by which data was stored
when it was collected during Summer 2023.

This class contains all the methods to convert from non-standard to standard
format as well as other methods to handle data collections in standard format
to make them compatible with other functions in the program.

Data collections for ``Excess Path Length``, ``Allan Variance``, and ``Correlation`` follow variations of the standard format
```
standard_excess_path_length = {'specifications': {'filter_number':b'IA=%d',
                                                  'units': {'pressures':str,
                                                            'times':str,
                                                            'L_norm':str='mm',
                                                            'p_norm':str='bar'
                                                           },
                                                  'stations':[],
                                                  'sampling_frequency':int,     
                                                  },
                               'excess_path_length':{'station_pair':[]},
                               'times':{'station_pair':[]}    
                              }
```

```
standard_allan_variance = {'specifications': {'filter_number':b'IA=%d',
                                              'units': {'allan_var':str='Phase',
                                                        'times':str,
                                                        'pressures':str
                                                       },
                                              'stations':[],
                                              'sampling_frequency':int
                                             },
                           'times':{'station_pair':[]},
                           'allan_var':{'station_pair':[]}
                          }
```

```
standard_correlation = {'specifications': {'filter_number':b'IA=%d',
                                           'units': {'pressures':str,
                                                     'times':str,
                                                     'frequency':str='Hz'
                                                    }
                                           'stations':[],
                                           'sampling_frequency':int
                                          },
                        'cross':{'frequencies':{'station_pairs':[]},
                                 'correlation_norm':{'station_pairs':[]},
                                 'correlation':{'station_pairs':[]}
                                },
                        'auto':{'frequencies':{'station_pairs':[]},
                                'correction_norm':{'station_pairs':[]},
                                'correlation':{'station_pairs':[]}
                               }
                       }
```


Methods
-------
load(collection_path:str)
    Returns the specified pickle file containing a data collection in standard format

load_old(path:str, collection_name:str)
    Returns the specified pickle file containing a data collection in non-standard format

get_filter(data_dict:dict)
    Returns the filter setting by which a data collection in standard format was taken

get_filter_old(data_dict:dict)
    Returns the filter setting by which a data collection in non-standard format was taken

reformat(path:str, collection_name:str,
         station_names:list=['dol', 'ott', 'sea', 'orc'],
         pressure_units:str='bar', time_units:str='sec')
    Returns a reformatted data collection in standard format

save(data_dict:dict, file_path:str)
    Stores the data collection as a pickle file in the specified path
"""

import pickle

def load(collection_path:str):
    """Retrieves and loads a pickle file of the collection into a dictionary
    
    Parameters
    ----------
    collection_path : str
        The full path of the pickle file which contains the collection data of all stations

    Returns
    -------
    data_dict : dict
        A dictionary containing the entire data collection
    """
    with open(collection_path, "rb") as f:
        return pickle.load(f)        

def load_old(path:str, collection_name:str):
    """Retrieves and loads a specific pickle files of a collection before 2024 into a dictionary
    
    Parameters
    ----------
    path : str
        The path to the directory in which the data collection is stored

    collection_name : str
        The path where the pickle file is stored

    Returns
    -------
    data_dict : dict
        A dictionary containing all the data collection
    """
    data_dict = {}
    sea_mammals = ['dolphin', 'otter', 'seal', 'orca']

    for idx in range(len(sea_mammals)):

        dictionary_name = 'data_dict_' + (sea_mammals[idx])[0:3]
        pickle_file_name = sea_mammals[idx] + '_' + collection_name

        with open(path + pickle_file_name, "rb") as f:
            dictionary_name = pickle.load(f)
        data_dict[idx] = (dictionary_name)

    return data_dict

def get_filter(data_dict:dict):
    """Retrieves the filter setting of the data collection
    
    Parameters
    ----------
    data_dict : str
        The data collection in standard format

    Returns
    -------
    filter_number : bytes
        The filter setting in bytes
    """
    filter_number = data_dict['specifications']['filter']

    return filter_number

def get_filter_old(data_dict:dict):
    """Retrieves the filter setting of the non-reformatted data collection
    
    Parameters
    ----------
    data_dict : str
        The data collection

    Returns
    -------
    filter_number : bytes
        The filter setting in bytes
    """
    filter_number = str(data_dict[0].keys())
    filter_number = filter_number.split('=')
    filter_number = filter_number[1].split('\'')
    filter_number = int(filter_number[0])
    filter_number = b'IA=%d' % filter_number

    return filter_number

def reformat(path:str, collection_name:str,
             station_names:list=['dol', 'ott', 'sea', 'orc'],
             pressure_units:str='bar', time_units:str='sec',
             sampling_frequency:int=625):
    """Reformats collections before 2024 into new standard collection format
    
    Parameters
    ----------
    old_collection : dict
        A dictionary containing collection data after being processed using load_old()

    station_names : list
        A list of all the station names which will be used as keys for the reformatted dictionary
        Note: Make sure the order of the station names are in the same order as in old_collection
        (default ['dol', 'ott', 'sea', 'orc'] - order for collections before 2024)

    pressure_units : str
        The unit of pressure in which old_collection was taken
        (default 'bar')

    time_units : str
        The unit of time in which old_collection was taken
        (default 'sec')

    Returns
    -------
    data_dict : dict
        The reformatted dictionary containing the entire collection
    """
    old_collection = load_old(path, collection_name)
    filter_num = get_filter_old(old_collection)

    new_dict = {}
    new_dict['specifications'] = {'filter':filter_num,
                                  'units':{'pressures':pressure_units,
                                           'times':time_units},
                                  'stations':station_names,
                                  'sampling_frequency':sampling_frequency}

    data_dict = {}
    for idx in range(len(station_names)):
        p_arr = old_collection[idx][filter_num]['pressures']
        time_arr = old_collection[idx][filter_num]['times']
        
        reformatted_dict = {}
        reformatted_dict = {'pressures':p_arr, 'times':time_arr}

        data_dict[station_names[idx]] = reformatted_dict
    
    #Brought out of loop - To be tested
    new_dict['data'] = data_dict

    return new_dict

def save(data_dict:dict, file_path:str):
    """Stores the given dataset as a pickle file at the given path

    Parameters
    ----------
    data_dict : dict
        The data collection that will be stored as a pickle file
    
    file_path : str
        The full path at which the pickle file will be saved including the name of the pickle file
    """
    with open(file_path, "wb") as f:
        pickle.dump(data_dict, f)