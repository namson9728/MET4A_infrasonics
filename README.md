# MET4A_infrasonics

This repository contains the refactored code from the original MET4A repository: https://github.com/kartographer/met4a.git

Requirements:
    - numpy
    - matplotlib
    - pickle

Basic Data File =   { b'IA=#': {ott:{pressures:[#,#,...,#], times:[#,#,...,#]},
                                orc:{pressures:[#,#,...,#], times:[#,#,...,#]},
                                dol:{pressures:[#,#,...,#], times:[#,#,...,#]},
                                sea:{pressures:[#,#,...,#], times:[#,#,...,#]},
                    }
                    }

    1. The datafile consists of an outer dictionary with one key being the filter number

    2. Associated with the filter number is an inner dictionary with four more keys: ['ott', 'orc', 'dol', 'sea']

    2. Each inner key is associated with another sub dictionary with two sub keys: ['pressures', 'times']

    3. Associated with each sub key is the respective data measurements


Cross-correlation Data File =   { b'IA=#': {'ott-ott':[#,#,...,#],
                                            'ott-orc':[#,#,...,#],
                                            'ott-dol':[#,#,...,#],
                                            'ott-sea':[#,#,...,#],
                                            'orc-orc':[#,#,...,#],
                                            'orc-dol':[#,#,...,#],
                                            'orc-sea':[#,#,...,#],
                                            'dol-dol':[#,#,...,#],
                                            'dol-sea':[#,#,...,#],
                                            'sea-sea':[#,#,...,#]
                                }
                                }

    1. The datafile consists of an outer dictionary with one key being the filter number

    2. Associated with the filter number is an inner dictionary with all the station combinations as the keys

    3. Each inner key is associated with the respective data measurements

There are two main data collection formats: standard and non-standard

As the name suggests, standard format is the standard way a data collection
is store to simplify the data analysis process.
```Python
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

```Python
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

```Python
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

```Python
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


Uses of MET4A Infrasonics:

    - Calculate excess path length, correlation, allan variance, interferometric response
        1. Load pickle data into dictionary
        2. Extract raw data from dictionary
        3. Use raw data to do calculations
        4. Store new data into dictionary
        5. Save new dictionary as pickle file

    - Plot timeseries, allan variance, correlation, interferometric response
        1. Load pickle data into dictionary
        2. Extract raw data from dictionary
        3. Use raw data and specifications to plot

    - Connect to bot to collect data using MET4A instruments
        1. Set-up bot specifications
        2. Run script on raspberry pi to establish connection to Slack channel with specifications