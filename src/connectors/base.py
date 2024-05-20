from abc import ABC

class BaseConnector(ABC):
    '''
    Abstract Connector to generate path to a twitch video
    '''
    def get_vod_path(self, url: str, quality: str, verbose: bool) -> str:
        pass