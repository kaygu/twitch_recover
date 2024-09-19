import hashlib
import os
import requests
from typing import List, Iterable

from connectors.base import BaseConnector
from utils.enums import HTTPStatusCode
from utils.files import load_domains

class TwitchConnector(BaseConnector):
    auth_api_url = "https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
    video_api_url = "https://api.twitch.tv/helix/videos?id={VIDEO_ID}"
    videos_api_url = "'https://api.twitch.tv/helix/videos?user_id={USER_ID}"

    def __init__(self):
        super().__init__()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')

        self.domains = load_domains()

        # Request bearer token
        # self._generate_token()


    # def _generate_token(self):
    #     req = requests.post(self.auth_api_url.format(CLIENT_ID=self.client_id, CLIENT_SECRET=self.client_secret))
    #     if req.status_code == HTTPStatusCode.OK:
    #         response = req.json()
    #         self.token = response.get('access_token')
    #         self.token_expiration = response.get('expires_in')
    #         if self.token:
    #             print(self.token)
    #             print("expires: " + str(self.token_expiration))
    #     else:
    #         raise Exception("Authentification failed")
        
    def get_vod(self, streamer_name: str, vodID: int, timestamp: int, quality: str = 'chunked', verbose: bool = False) -> str:
        '''
        Generates url to m3u8 file
        '''
        base_path = f"{streamer_name}_{vodID}_{timestamp}"
        h = hashlib.sha1(base_path.encode())
        hash = h.hexdigest()[:20]
        path = f"/{hash}_{base_path}/{quality}/index-dvr.m3u8"
        if verbose:
            print(f'path: {path}')
        return self._find_host(path, verbose)
    

    def _find_host(self, path: str, verbose: bool = False) -> str:
        '''
        Find the matching hostname for the VOD path
        '''
        for host in self.domains:
            url = host + path
            r = requests.get(url)
            if r.status_code == HTTPStatusCode.FORBIDDEN:
                if verbose:
                    print("Denied: " + url)
            if r.status_code == HTTPStatusCode.OK:
                if verbose:
                    print("Success: " + url)
                return url
        return None
