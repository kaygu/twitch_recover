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
    status = response.status_code
    ct = response.headers.get('Content-Type')
    if status == 200 and (ct == 'video/MP2T' or ct == 'binary/octet-stream'):
        return True
    return False

def download_transport_stream(path: str, url: str) -> bool:
    '''
    Downloads a .ts file and saves it in a directory
    return: True if success, False if failure
    '''
    # headers = {"User-Agent": "Mozilla/5.0"}
    if check_file(path):
        r = requests.get(url)
        if is_downloadable(r):
            with open(path, 'wb') as download:
                download.write(r.content)
        else:
            if r.status_code != 403:
                print(f'{url} could not be downloaded\nstatus code: {r.status_code}\n{r.headers}')
