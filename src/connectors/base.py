from abc import ABC
from typing import List

class BaseConnector(ABC):
    '''
    Abstract Connector to generate path to a twitch video
    '''
    def get_vod_path(self, url: str, quality: str, verbose: bool = False) -> str:
        pass
    
    def get_past_vods(self, streamer: str, verbose: bool = False) -> List[tuple]:
        pass