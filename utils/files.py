import os
import time
import shutil

def clean_files(vid_dir: str, m3u8_file: str, verbose: bool = False):
    '''
    Clean the mess after the video conversion
    '''
    start_time = time.time()  # Start timing
    if os.path.exists(m3u8_file):
        os.remove(m3u8_file)
    if os.path.exists(vid_dir):
        shutil.rmtree(vid_dir)
    end_time = time.time()  # End timing
    if verbose:
        print(f"Cleaning files time taken: {end_time - start_time:.2f} seconds") 

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