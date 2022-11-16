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

def find_vod_path(url: str) -> str:
    '''
    Find VOD for a TwitchTracker url
    '''
    result = re.search(r'https://twitchtracker.com/(\w+)/streams/(\d+)',url)
    if not result:
        raise Exception('Not a valid TwitchTracker vod link')
    name = result.group(1)
    print(f'Searching for VOD of streamer {name}')
    vodID = result.group(2)
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        result = re.search(r' stream on (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', req.text)
        print(f'Stream recorded on {result.group(1)}')
        timestamp = calendar.timegm(time.strptime(result.group(1), '%Y-%m-%d %H:%M:%S'))
    else:
        raise Exception('TwitchTracker status code returned', req.status_code, req.headers)
    
    base_path = f"{name}_{vodID}_{timestamp}"
    h = hashlib.sha1(base_path.encode())
    hash = h.hexdigest()[:20]
    quality = "chunked" # best quality
    PATH = f"/{hash}_{base_path}/{quality}/index-dvr.m3u8"
    return PATH

def find_vod_host(path: str) -> str:
    # find correct hostname
    domains = load_domains()
    for host in domains:
        url = host + path
        r = requests.get(url)
        if r.status_code == 200:
            break
    return url