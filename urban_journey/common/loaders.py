"""Package containing functions to load data files into dtst."""

import numpy as np
import os.path

def load_csv(filename, skip_rows=0):
    """Function to load data from an csv file.
    
    Parameters
    ----------
    filename : string
        Relative location of the csv file.
    skip_rows : integer, optional
        Number of lines at the top of the file that do not contain any data
        (default is 0).
    
    Returns
    -------
    data : numpy_array
        Data from the csv file.
        
    Raises
    ------
    IOError
        If the file is not found.
    TypeError
        If the file is not a csv file.
    """
    if not os.path.isfile(filename):
        raise IOError('File not found')
    
    ext = os.path.splitext(filename)[1]
    
    if ext is not '.csv':
        raise TypeError('File is not of type csv')
    
    np.loadtxt(open(filename,"rb"),delimiter=",",skiprows = skip_rows)