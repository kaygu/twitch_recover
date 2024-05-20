import calendar
import hashlib
import re
import requests
import time

from src.connectors.base import BaseConnector
from src.enums import HTTPStatusCode

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106"}

class TwitchTrackerConnector(BaseConnector):
    def get_vod_path(self, url: str, quality: str, verbose: bool) -> str:
        result = re.search(r'https:\/\/twitchtracker.com\/(\w+)\/streams\/(\d+)', url)
        if not result:
            raise Exception('Not a valid TwitchTracker video link')
        name = result.group(1)
        if verbose:
            print(f'Searching for VOD of streamer {name}')
        vodID = result.group(2)
        req = requests.get(url, headers=headers)
        if req.status_code == HTTPStatusCode.OK:
            result = re.search(r' stream on (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', req.text)
            if not result:
                raise Exception('Could not find timestamp in TwitchTracker page')
            if verbose:
                print(f'Stream recorded on {result.group(1)}')
            timestamp = calendar.timegm(time.strptime(result.group(1), '%Y-%m-%d %H:%M:%S'))
        elif req.status_code == HTTPStatusCode.NOT_FOUND:
            raise Exception('404 TwitchTracker video not found')
        else:
            raise Exception('TwitchTracker status code returned', req.status_code, req.headers)
        
        base_path = f"{name}_{vodID}_{timestamp}"
        h = hashlib.sha1(base_path.encode())
        hash = h.hexdigest()[:20]
        PATH = f"/{hash}_{base_path}/{quality}/index-dvr.m3u8"
        return PATH