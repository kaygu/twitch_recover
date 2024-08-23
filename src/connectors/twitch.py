import calendar
import hashlib
import os
import re
import requests
import time
from typing import List

from src.connectors.base import BaseConnector
from src.utils.enums import HTTPStatusCode

class TwitchConnector(BaseConnector):
    auth_api_url = "https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
    video_api_url = "https://api.twitch.tv/helix/videos?id={VIDEO_ID}"
    videos_api_url = "'https://api.twitch.tv/helix/videos?user_id={USER_ID}"

    def __init__(self) -> None:
        super().__init__()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')

        # Request bearer token
        self.generate_token()


    def generate_token(self):
        req = requests.post(self.auth_api_url.format(CLIENT_ID=self.client_id, CLIENT_SECRET=self.client_secret))
        if req.status_code == HTTPStatusCode.OK:
            response = req.json()
            self.token = response.get('access_token')
            self.token_expiration = response.get('expires_in')
            if self.token:
                print(self.token)
                print("expires: " + str(self.token_expiration))
        else:
            raise Exception("Authentification failed")
        
    def get_vod_path(self, url: str, quality: str, verbose: bool) -> str:
        result = re.search(r'https:\/\/www.twitch.tv\/videos\/(\d+)', url)
        if not result:
            raise Exception('Not a valid Twitch video link')
        vidID = result.group(1)
        header = {'Authorization': f'Bearer {self.token}', 'Client-Id': self.client_id}
        req = requests.get(self.video_api_url.format(VIDEO_ID=vidID), headers=header)
        if req.status_code == HTTPStatusCode.OK:
            if verbose:
                print(req.json())
        else:
            #TODO: If 401, refresh bearer token & retry
            raise Exception("Failed request/ Status code " + str(req.status_code))
        
        result = req.json()
        video = result.get('data')[0]
        
        # created_at date gives different timestamp than in the VOD path
        # timestamp = calendar.timegm(time.strptime(video['created_at'], '%Y-%m-%dT%H:%M:%SZ')) 
        
        # TODO: Handle Key error 
        thumbnail_url = video['thumbnail_url']
        re_result = re.search(r'https:\/\/.+\/cf_vods\/(.+)\/(.+)\/\/thumb\/thumb0-%{width}x%{height}\.jpg', thumbnail_url)
        if not re_result:
            raise Exception('Thumbnail URL was not valid')
        sub_domain = re_result.group(1)
        vod_path = re_result.group(2)
        if verbose:
            print(f'sub-domain {sub_domain}')
            print(f'hash {vod_path}')

        PATH = None
        if video['type'] == 'highlight':
            PATH = f'/{vod_path}/{quality}/highlight-{video["id"]}.m3u8'
        else:
            PATH = f'/{vod_path}/{quality}/index-dvr.m3u8'
        return PATH
    
    def get_past_vods(self, streamer: str, verbose: bool = False) -> List[str]:
        pass
        # header = {'Authorization': f'Bearer {self.token}', 'Client-Id': self.client_id}
        # req = requests.get(self.videos_api_url.format(USER_ID=streamer), headers=header)
        # if req.status_code == HTTPStatusCode.OK:
        #     if verbose:
        #         print(req.json())
        # else:
        #     #TODO: If 401, refresh bearer token & retry
        #     raise Exception("Failed request/ Status code " + str(req.status_code))

        # Get USER ID 
        ## https://api.twitch.tv/helix/users?login=aleczandxr
        # Get vods
        ## https://api.twitch.tv/helix/videos?user_id=148374967