

class data:
    """
    A class that contains all the methods to handle datasets

    ...

    Attributes
    ----------
    collection_name : str
        name of the data collection
        (default None)

    dataset_names : str array
        list of all the identifying names of each dataset
        (default ['ott', 'orc', 'dol', 'sea'])

    filter_number : int
        the filter setting of the MET4A barometer used during collection of the dataset

    data_path : str
        the path to where the data collection is stored
        (default './')
        
    out_path : str
        the desired path where data may be stored
        (default './')

    Methods
    -------
    save(collection_name, out_path='./')
        Stores the data collection or dataset as a pickle file

    load()
        Retrieves the specified pickle file

    split(collection_name, dataset_names, data_path='./', out_path='./')
        Divides the given dataset into individual dictionaries to save as multiple pickle files

    join(collection_name, dataset_names, data_path='./', out_path='./')
        Combines a group of related datasets into one dictionary and saves it as a single pickle file
    """

    def __init__(self, filter_number:int, dataset_names=['ott','orc','dol','sea'],
                 collection_name=None, sampling_rate=625, data_path='./', out_path='./'):
        """
        Parameters
        ----------
        dataset_names : str(list)
            The list of all the identifying names of each dataset
            (default ['ott', 'orc', 'dol', 'sea'])

        filter_number : int
            The filter setting of the MET4A barometer used during collection of the dataset

        collection_name : str, optional
            The name of the data collection within which are a number of datasets
            (default None)

        sampling_rate : int, optional
            The sampling rate used during collection of the dataset
            (default 625)

        data_path : str, optional
            The path to where the data collection is stored
            (default './')

        out_path : str, optioanl
            The desired path where data may be stored
            (default './')
        """

        self.collection_name = collection_name
        self.dataset_names = dataset_names
        self.filter_number = filter_number
        self.sampling_rate = sampling_rate
        self.data_path = data_path
        self.out_path = out_path

    def save(self, pickle_name:str, path:str):
        """Stores the given dataset as a pickle file at the given path

        Parameters
        ----------
        pickle_name : str
            The name by which the pickle file will be saved
        
        path : str
            The path at which the pickle file will be saved
            (default './)
        """
        print(pickle_name, path)

    def load(self, pickle_name:str, path:str):
        """Retrieves and loads the specified pickle file into a dictionary
        
        Parameters
        ----------
        pickle_name : str
            The name of the pickle file to be retrieved

        path : str
            The path where the pickle file is stored
        """
        print(pickle_name, path)

    def split(collection_name, dataset_names, data_path='./', out_path='./'):
        """Divides the given dataset into individual dictionaries where each dataset name will be:
                collection_name + '_' + dataset_name

        Parameters
        ----------
        collection_name : str
            The name of the data collection within which are a number of datasets

        dataset_names : str(list)
            The list of all the identifying names of each dataset

        data_path : str, optional
            The path to where the data collection is stored
            (default './')

        out_path : str, optioanl
            The desired path where data will be stored
            (default './')
        """
        pass

    def join(collection_name, dataset_names, data_path='./', out_path='./'):
        """Combines a group of related datasets into one dictionary and saves it as a single pickle file
        Parameters
        ----------
        collection_name : str
            The name of the data collection within which are a number of datasets

        dataset_names : str(list)
            The list of all the identifying names of each dataset

        data_path : str, optional
            The path to where the data collection is stored
            (default './')

        out_path : str, optioanl
            The desired path where data will be stored
            (default './')
        """
        pass