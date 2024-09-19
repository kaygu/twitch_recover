import os
import requests

from utils.enums import HTTPStatusCode

def does_exist(path: str) -> bool:
    '''
    Check if Transport Stream File (.ts) is already downloaded
    '''
    if os.path.exists(path):
        return True
    return False

def is_downloadable(response: requests.Response) -> bool:
    '''
    Check if the response the a request is a dowloadable Transport Stream File (.ts)
    '''
    ct = response.headers.get('Content-Type')
    if response.status_code == HTTPStatusCode.OK and (ct == 'video/MP2T' or ct == 'binary/octet-stream'):
        return True
    return False