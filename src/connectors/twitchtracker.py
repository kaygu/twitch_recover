import calendar
from bs4 import BeautifulSoup
import hashlib
import re
from typing import List
import requests
import time

from connectors.base import BaseConnector
from utils.enums import HTTPStatusCode

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.106"}

class TwitchTrackerConnector(BaseConnector):
    streams_url = "https://twitchtracker.com/{STREAMER_NAME}/streams"

    def get_vod_path(self, url: str, quality: str, verbose: bool = False) -> str:
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
    
    def get_past_vods(self, streamer: str, verbose: bool = False) -> List[tuple]:
        # Current method requires stream ID to get the exact start timestamp, 
        # which does not seem possible without using the TT API or using Selenium.
        # Stream page (https://twitchtracker.com/{STREAMER_NAME}/streams) only provides stream dates without precision and no link to the stream
        # Giving up on TwitchTracker method for now 
        pass
        

        # req = requests.get(self.streams_url.format(STREAMER_NAME=streamer), headers=headers)
        # if req.status_code == HTTPStatusCode.OK:
        #     soup = BeautifulSoup(req.text, 'html.parser')
            
        #     print("last streams: ")
        #     for tr in soup.find(id="streams").tbody.find_all('tr'):
        #         stream_id = tr.a.get('href') #Does not work, stream_id is provided later via js, it's not in the source
        #         datetime, duration = (n.get('data-order') for n in tr.find_all_next('td', limit=2))
        #         #GET STREAM ID TOO !!! 
        #         if verbose:
        #             print(f"{datetime}, {duration}. ID: {stream_id}")
                
        #     print('----')
        #     # TODO: Keep the VOD's in the past 60 days. Return them as a list of tuples
        # else:
        #     print(f"Status code {req.status_code}")
            