import os
import requests

def create_dir(name: str):
    '''
    Create directory where .ts files will be stored
    '''
    if not os.path.exists(name):
        os.mkdir(name)

def check_file(name: str) -> bool:
    '''
    Check if Transport Stream File (.ts) is already downloaded
    return: True if does not exist, False if it already exists
    '''
    if os.path.exists(name):
        return False
    return True

def is_downloadable(response: requests.Response) -> bool:
    '''
    Check if a url directs to a dowloadable Transport Stream File (.ts)
    param url: Path to the file to check
    return: bool
    '''
    ct = response.headers.get('Content-Type')
    if ct == 'video/MP2T':
        return True
    return False

def download_transport_stream(path: str, url: str) -> bool:
    '''
    Downloads a .ts file and saves it in a directory
    return: True if success, False if failure
    '''
    if check_file(path):
        r = requests.get(url)
        if is_downloadable(r):
            with open(path, 'wb') as download:
                download.write(r.content)
        else:
            print(f'{path} could not be downloaded')
