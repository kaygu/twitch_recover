import calendar
import hashlib
import re
import requests
import time


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106"}

def load_domains():
    with open('domains.txt', 'r') as f:
        DOMAINS = f.read().splitlines()
    return DOMAINS

def generate_vod_path(twitch_tracker_url: str, quality: str = "chunked", verbose: bool = False) -> str:
    '''
    Generate VOD for a TwitchTracker url
    param twitch_tracker_url: URL to the TwitchTracker VOD
    param quality: Quality of the twitch VOD
    return: Path to the VOD (m3u8 file)
    '''
    result = re.search(r'https://twitchtracker.com/(\w+)/streams/(\d+)', twitch_tracker_url)
    if not result:
        raise Exception('Not a valid TwitchTracker video link')
    name = result.group(1)
    if verbose:
        print(f'Searching for VOD of streamer {name}')
    vodID = result.group(2)
    req = requests.get(twitch_tracker_url, headers=headers)
    if req.status_code == 200:
        result = re.search(r' stream on (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', req.text)
        if not result:
            raise Exception('Could not find timestamp in TwitchTracker page')
        if verbose:
            print(f'Stream recorded on {result.group(1)}')
        timestamp = calendar.timegm(time.strptime(result.group(1), '%Y-%m-%d %H:%M:%S'))
    elif req.status_code == 404:
        raise Exception('404 TwitchTracker video not found')
    else:
        raise Exception('TwitchTracker status code returned', req.status_code, req.headers)
    
    base_path = f"{name}_{vodID}_{timestamp}"
    h = hashlib.sha1(base_path.encode())
    hash = h.hexdigest()[:20]
    PATH = f"/{hash}_{base_path}/{quality}/index-dvr.m3u8"
    return PATH

def generate_vod_path_offline(twitch_tracker_url: str, date: str, quality: str = "chunked", verbose: bool = False) -> str:
    '''
    Generate VOD for a TwitchTracker url (offline version)
    param twitch_tracker_url: URL to the TwitchTracker VOD
    param date: Date of the stream
    param quality: Quality of the twitch VOD
    return: Path to the VOD (m3u8 file)
    '''
    result = re.search(r'https://twitchtracker.com/(\w+)/streams/(\d+)', twitch_tracker_url)
    if not result:
        raise Exception('Not a valid TwitchTracker video link')
    steamer_name = result.group(1)

    if verbose:
        print(f'Searching for VOD of streamer {steamer_name}')
    vodID = result.group(2)
    try:
        timestamp = calendar.timegm(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
    except:
        raise Exception('Invalid date format')
    
    base_path = f"{steamer_name}_{vodID}_{timestamp}"
    h = hashlib.sha1(base_path.encode())
    hash = h.hexdigest()[:20]
    PATH = f"/{hash}_{base_path}/{quality}/index-dvr.m3u8"
    return PATH

def find_vod_host(path: str, verbose: bool = False) -> str:
    '''
    Find the matching hostname for the VOD path
    param path: Path to the VOD
    return: URL to the VOD
    '''
    domains = load_domains()
    for host in domains:
        url = host + path
        r = requests.get(url)
        if r.status_code == 403:
            if verbose:
                print("Denied: " + url)
        if r.status_code == 200:
            if verbose:
                print("Success: " + url)
            return url
    return None