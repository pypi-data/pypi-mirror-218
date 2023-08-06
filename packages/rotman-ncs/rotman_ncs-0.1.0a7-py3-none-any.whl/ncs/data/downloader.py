import os
import zipfile
import urllib.request


def download_and_extract(url, dest_dir_name):
    # Get the home directory
    if os.name == 'nt':  # For Windows
        base_dir = os.getenv('APPDATA')
    else:  # For Linux/OS X
        base_dir = os.path.expanduser('~')

    dest_dir = os.path.join(base_dir, dest_dir_name)

    # Create the directory if it does not exist
    os.makedirs(dest_dir, exist_ok=True)

    # Define the paths
    zip_path = os.path.join(dest_dir, 'ncs_data.zip')
    data_dir = os.path.join(dest_dir, 'ncs_data')

    # Custom function to handle block reading from url and writing to file
    def _report(count, block_size, total_size):
        percent = count * block_size * 100 // total_size
        print(f'\rDownload progress: {percent}%', end='')

    # Download the file from url and save it locally under zip_path:
    urllib.request.urlretrieve(url, zip_path, reporthook=_report)
    print('\nDownload finished. Extracting files...')

    # Create a ZipFile Object
    with zipfile.ZipFile(zip_path) as zip_file:
        # Extract all the contents of zip file in the data directory
        zip_file.extractall(data_dir)

    print(f'Data downloaded and extracted to {data_dir}')
