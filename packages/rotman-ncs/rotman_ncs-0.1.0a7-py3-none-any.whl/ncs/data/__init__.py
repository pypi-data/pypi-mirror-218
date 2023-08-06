import os
import pandas as pd

from ncs.data.downloader import download_and_extract


def data_folder():
    """
    Retrieves the path to the data folder.

    The data folder is in the user's home directory on Linux (i.e. /home/username/rotman_ncs_data/ncs_data) 
    and on Windows (i.e. C:\\Users\\username\\AppData\\Roaming\\rotman_ncs_data\\ncs_data).

    Returns:
        str: The path to the data folder.
    """

    if os.name == 'nt':  # For Windows
        base_dir = os.getenv('APPDATA')
    else:  # For Linux/OS X
        base_dir = os.path.expanduser('~')

    dest_dir = os.path.join(base_dir, 'rotman_ncs_data', 'ncs_data')

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    return dest_dir


def check_data_exist_and_download(data_file):
    """
    Check if the given data file exists and download it if it does not.

    Parameters:
        data_file (str): The path to the data file.

    Returns:
        None
    """
    if not os.path.exists(data_file):
        download_and_extract(
            'https://storage.googleapis.com/rotman-ncs-data-buket/ncs_data.zip', 'rotman_ncs_data')


def load_stock_returns_on_calls(data_type='train'):
    """
    Load stock returns on calls data.

    Args:
        data_type (str): The type of data to load (train or test). Defaults to 'train'.

    Returns:
        DataFrame: The loaded stock returns on calls data.
    """
    data_file = f'{data_folder()}/{data_type}/stock_return_data.parquet'
    check_data_exist_and_download(data_file)
    return pd.read_parquet(data_file)


def load_stock_history():
    """
    Load the stock price history data.

    Returns:
        pd.DataFrame: The stock price history data.
    """
    data_file = f'{data_folder()}/all_stock_price_history.parquet'
    check_data_exist_and_download(data_file)
    return pd.read_parquet(data_file)


def load_call_description(data_type='train'):
    """
    Load the earnings call description data from the specified data type.

    Parameters:
        data_type (str, optional): The type of data to load (train or test). Defaults to 'train'.

    Returns:
        DataFrame: The loaded call description data.
    """
    data_file = f'{data_folder()}/{data_type}/call_data.parquet'
    check_data_exist_and_download(data_file)
    return pd.read_parquet(data_file)


def load_call_statements(data_type='train'):
    """
    Load the earnings call statements data from a specified data type.

    Parameters:
        data_type (str): The type of data to load (train or test). Default is 'train'.

    Returns:
        pandas.DataFrame: The loaded call statements data.
    """
    data_file = f'{data_folder()}/{data_type}/call_statement_data.parquet'
    check_data_exist_and_download(data_file)
    return pd.read_parquet(data_file)
