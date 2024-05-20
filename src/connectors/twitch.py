import calendar
import hashlib
import os
import re
import requests
import time

from src.connectors.base import BaseConnector
from src.enums import HTTPStatusCode

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
            print("Authentification failed")
        
    def get_vod_path(self, url: str, quality: str, verbose: bool) -> str:
        result = re.search(r'https:\/\/www.twitch.tv\/videos\/(\d+)', url)
        if not result:
            raise Exception('Not a valid Twitch video link')
        vidID = result.group(1)
        header = {'Authorization': f'Bearer {self.token}', 'Client-Id': self.client_id}
        req = requests.get(self.video_api_url.format(VIDEO_ID=vidID), headers=header)
        if req.status_code == HTTPStatusCode.OK:
            print(req.json())
        else:
            # If 401, refresh bearer token & retry
            raise Exception("Failed request/ Status code " + str(req.status_code))
        
        result = req.json()
        video = result.get('data')[0]
        
        timestamp = calendar.timegm(time.strptime(video['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
        base_path = f"{video['user_login']}_{video['stream_id']}_{timestamp}"
        h = hashlib.sha1(base_path.encode())
        hash = h.hexdigest()[:20]
        PATH = f"/{hash}_{base_path}/{quality}/index-dvr.m3u8"
        return PATH