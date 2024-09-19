from abc import ABC
from typing import List, Iterable

class BaseConnector(ABC):
    '''
    Abstract Connector to generate path to a twitch video
    '''
    def get_vod(self, streamer_name: str, vodID: int, timestamp: int, quality: str = 'chunked', verbose: bool = True) -> str:
        pass
    
    def get_past_vods(self, streamer: str, verbose: bool = False) -> Iterable[tuple]:
        pass