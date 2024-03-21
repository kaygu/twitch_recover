import os

def create_dir(name: str):
    '''
    Create directory where .ts files will be stored
    param name: Name of the directory
    '''
    if not os.path.exists(name):
        os.mkdir(name)

def check_file(name: str) -> bool:
    '''
    Check if Transport Stream File (.ts) is already downloaded
    param name: Path to the file to check
    return: True if does not exist, False if it already exists
    '''
    if os.path.exists(name):
        return False
    return True