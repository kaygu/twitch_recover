import requests

from utils.files import create_dir, check_file

def download_vod(m3u8_url: str, path: str, verbose: bool = False):
    '''
    Downloads a VOD from a m3u8 file
    param m3u7_url: URL to the m3u8 file
    param path: path to save the files
    '''
    r = requests.get(m3u8_url)
    base_url = m3u8_url.rpartition('/')[0]
    m3u8 = r.text
    vod_name = path
    create_dir(vod_name)

    for record in m3u8.splitlines():
      if not record.startswith('#') and record != '':
          if '-unmuted.ts' in record:
              record_name = record.replace('-unmuted.ts', '.ts')
              record_muted = record.replace('-unmuted.ts', '-muted.ts')
              #download original file
              if not download_ts_file(vod_name + '/' + record_name, base_url + '/' + record_name):
                  #if failed, download muted file (backup)
                  download_ts_file(vod_name + '/' + record_name, base_url + '/' + record_muted) 
              else:
                  if verbose:
                      print(f"Muted segment {record_name} was recovered")
          else:
              download_ts_file(vod_name + '/' + record, base_url + '/' + record)

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

def download_ts_file(path: str, url: str) -> bool:
    '''
    Downloads a .ts (transport stream) file and saves it in a directory
    param path: path to save the file
    param url: URL to the .ts file
    return: True if success, False if failure
    '''
    if check_file(path):
        r = requests.get(url)
        if is_downloadable(r):
            with open(path, 'wb') as download:
                download.write(r.content)
                return True
        else:
            if r.status_code != 403:
                raise Exception(f'{url} could not be downloaded\nstatus code: {r.status_code}\n{r.headers}')
    return False


def has_muted(file: str) -> bool:
    '''
    Check if a portion of the stream is muted
    param file: m3u8 file content. Not the file path
    return: bool
    '''
    if '-unmuted.ts' in file:
        return True
    return False

def count_muted_segments(file: str) -> int:
    '''
    Returns the amount of muted segments present in the playlist
    param file: m3u8 file content. Not the file path
    return: muted segments count
    '''
    return file.count("-unmuted.ts")

def repair_muted_segments(file: str):
    '''
    Replaces all the muted segments with links that work
    param file: m3u8 file content. Not the file path
    return: modified m3u8 file content
    '''
    newFile = file.replace('-unmuted.ts', '-muted.ts')
    return newFile