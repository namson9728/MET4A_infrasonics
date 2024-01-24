# MET4A_infrasonics

This repository contains the refactored code from the original MET4A repository: https://github.com/kartographer/met4a.git

Below is a list of all the basic classes and their functions.

Requirements:
    - numpy
    - matplotlib
    - scipy
    - pickle

Specifications:
    - path
    - in-file name
    - station array
    - filter number
    - out-file name
    - sampling rate
    - 





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